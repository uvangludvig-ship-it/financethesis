#!/usr/bin/env python3
"""Compute structural metrics for SSE bachelor theses from pdftotext -layout output.

Usage: thesis_metrics.py <text_dir> <out_csv> [--index catalogue_index.json] [--winners old_winners/INDEX.md]
Each .txt in text_dir is one thesis; the stem is the MediumId (non-winners) or the winner filename.
"""
import csv, json, os, re, sys, statistics

TOP_JOURNALS = {
    'JF': r'Journal of Finance\b',
    'JFE': r'Journal of Financial Economics',
    'RFS': r'Review of Financial Studies',
    'JFQA': r'Journal of Financial and Quantitative Analysis',
    'RoF': r'Review of Finance\b',
    'QJE': r'Quarterly Journal of Economics',
    'AER': r'American Economic Review',
    'JPE': r'Journal of Political Economy',
    'ECMA': r'\bEconometrica\b',
    'REStud': r'Review of Economic Studies',
    'JME': r'Journal of Monetary Economics',
    'JET': r'Journal of Economic Theory',
    'JoE': r'Journal of Econometrics',
    'REStat': r'Review of Economics and Statistics',
    'JEL': r'Journal of Economic Literature',
}

METHODS = {
    'did': r'difference[- ]in[- ]difference|diff[- ]in[- ]diff|\bDiD\b|\bDD\b estimat',
    'event_study': r'event[- ]stud',
    'rdd': r'regression discontinuity',
    'iv': r'instrumental variable|two[- ]stage least|\b2SLS\b|\bIV\b (regression|approach|estimat|specification)',
    'fixed_effects': r'fixed[- ]effects?',
    'fama_macbeth': r'Fama[- ]?MacBeth',
    'panel': r'panel (data|regression|model)',
    'logit_probit': r'\blogit\b|\bprobit\b',
    'garch_var': r'\bGARCH\b|vector autoregress|\bVAR\b model',
    'portfolio_sorts': r'portfolio sort|decile portfolio|quintile portfolio|long[- ]short portfolio',
    'survey_interview': r'\bsurvey\b|questionnaire|\binterview',
    'case_study': r'case stud',
    'machine_learning': r'machine learning|neural network|random forest|\bLASSO\b',
    'structural_model': r'calibrat|structural model',
}

SOURCES = {
    'crsp_compustat': r'\bCRSP\b|Compustat',
    'wrds': r'\bWRDS\b',
    'bloomberg': r'Bloomberg',
    'datastream_refinitiv': r'Datastream|Refinitiv|Eikon|\bLSEG\b',
    'shof': r'Swedish House of Finance|\bSHoF\b|FinBas',
    'morningstar': r'Morningstar',
    'hand_collected': r'hand[- ]collect|manually collect',
    'statistics_sweden': r'Statistics Sweden|\bSCB\b',
    'finansinspektionen': r'Finansinspektionen',
    'capital_iq_orbis': r'Capital IQ|\bOrbis\b|Serrano|Retriever',
}

ANCHOR = r"we follow|following the (methodology|approach|method|framework|procedure|specification)|replicat|akin to|closely (follow|mimic|resembl)|based on the (methodology|approach|model|framework|specification) of|in line with the (methodology|approach) of|we adopt the (methodology|approach|method|specification)|we (employ|use|apply) the (same|methodology|approach|method)|methodology (of|used by|developed by|proposed by)|as in [A-Z][a-z]+ (and|&|et al)"
RQ_PHRASE = r'research question'
CONTRIB = r'to (our|the best of our) knowledge|first (study|paper|thesis) to|contribut(e|es|ion) to the literature|we contribute'
NULL_LANG = r'no (statistically |economically )?significant|not (statistically |economically )?significant|insignificant|fail(s|ed)? to reject|no evidence|cannot reject the null|do(es)? not find'
ROBUST = r'robustness'
PLACEBO = r'placebo'
PRETREND = r'parallel[- ]trend|pre[- ]trend|common trend'
SWEDISH = r'\bSweden\b|\bSwedish\b|\bStockholm\b|\bOMX|\bSEK\b|Nasdaq Stockholm|Riksbank'
NORDIC = r'\bNorway\b|\bNorwegian\b|\bDenmark\b|\bDanish\b|\bFinland\b|\bFinnish\b|\bNordic\b|\bOslo\b'
POLICY = r'\breform\b|regulation|natural experiment|quasi[- ](natural )?experiment|policy change|exogenous (shock|variation)|\bdirective\b|new law|introduction of the (law|tax|rule|regulation)'
HYPO = r'\b(?:H|Hypothesis\s*)(\d{1,2})\b'
QUAL = r'qualitative|thematic analysis|semi[- ]structured'

HEAD_INTRO = re.compile(r'^\s*(?:(?:1|I|1\.0)[\.\)]?\s+)?(?:Introduction|INTRODUCTION)\s*$', re.M)
HEAD_REFS = re.compile(r'^\s*(?:\d+[\.\)]?\s+|[IVX]+[\.\)]?\s+)?(?:References|REFERENCES|Bibliography|BIBLIOGRAPHY|Reference list|Reference List|List of references|List of References|Works Cited|Works cited|Literature list|Sources|Literature|Published Papers|Articles)(?:\s*$|\s{3,})', re.M)
HEAD_APPX = re.compile(r'^\s*(?:\d+[\.\)]?\s+|[IVX]+[\.\)]?\s+)?(?:Appendix|APPENDIX|Appendices|APPENDICES)\b|^\s*[A-H][\.\)]?\s{1,8}[A-Z][a-z]+[A-Za-z ,\-]{3,80}$', re.M)
NEXT_SECTION = re.compile(r'^\s*(?:2|II|2\.0)[\.\)]?\s+[A-Z][A-Za-z]', re.M)
NEXT_SECTION_NAMED = re.compile(r'^\s*(?:\d+[\.\)]?\s+)?(?:Literature|Previous|Related|Background|Theor|Data|Method|Hypothes|Institutional|Empirical|Research design)[A-Za-z &\-]*\s*$', re.M)


def count_refs(seg):
    """Count reference entries in a references segment (layout text)."""
    lines = seg.split('\n')
    entries = []
    cur = []
    for ln in lines:
        if not ln.strip():
            if cur:
                entries.append('\n'.join(cur)); cur = []
            continue
        indent = len(ln) - len(ln.lstrip(' '))
        if cur and indent <= 2 and re.match(r'\s{0,2}[A-ZÅÄÖÉ\[\(\"“]', ln):
            entries.append('\n'.join(cur)); cur = [ln]
        else:
            cur.append(ln)
    if cur:
        entries.append('\n'.join(cur))
    with_year = [e for e in entries if re.search(r'\b(19[5-9]\d|20[0-2]\d)[a-z]?\b', e)]
    # alternative: distinct author-year keys
    keys = set(re.findall(r'^\s{0,2}([A-ZÅÄÖ][A-Za-zÅÄÖåäöéü\'\-]+)[,\s].{0,200}?\b((?:19[5-9]|20[0-2])\d)[a-z]?\b', seg, re.M | re.S))
    return len(with_year), len(keys)


ENTRY_LINE = re.compile(r'^\s{0,3}(?:\[\d+\]\s*)?[A-ZÅÄÖ][\w\'\-]+.{0,160}?\b(?:19[5-9]|20[0-2])\d[a-z]?\b')


def fallback_refs_segment(text):
    lines = text.split('\n')
    n = len(lines)
    start_scan = int(n * 0.5)
    flags = [1 if ENTRY_LINE.match(l) else 0 for l in lines]
    best_i = None
    for i in range(start_scan, n - 15):
        if sum(flags[i:i + 15]) >= 6:
            best_i = i; break
    if best_i is None:
        return None
    start = sum(len(l) + 1 for l in lines[:best_i])
    appx = HEAD_APPX.search(text, start + 500)
    end = appx.start() if appx else len(text)
    return text[start:min(end, start + 60000)]


def find_refs_segment(text):
    heads = list(HEAD_REFS.finditer(text))
    if not heads:
        return fallback_refs_segment(text)
    # choose the heading followed by the most year-tokens before an appendix heading / end
    best = None
    for h in heads:
        start = h.end()
        appx = HEAD_APPX.search(text, start + 500)
        end = appx.start() if appx else len(text)
        seg = text[start:end]
        if len(seg) > 60000:
            seg = seg[:60000]
        score = len(re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b', seg))
        if best is None or score > best[0]:
            best = (score, seg)
    return best[1] if best and best[0] > 2 else None


def find_intro(text):
    heads = list(HEAD_INTRO.finditer(text))
    best = None
    for h in heads:
        start = h.end()
        m1 = NEXT_SECTION.search(text, start + 200)
        m2 = NEXT_SECTION_NAMED.search(text, start + 200)
        cands = [m.start() for m in (m1, m2) if m]
        end = min(cands) if cands else min(len(text), start + 20000)
        seg = text[start:end]
        if len(seg) > 40000:
            seg = seg[:40000]
        words = len(seg.split())
        # skip table-of-contents hits: too many dotted leaders / digits
        if seg.count('....') > 5 or words < 150:
            continue
        if best is None or words > best[0]:
            best = (words, seg)
    return best


def analyze(text):
    r = {}
    body = text
    r['words_total'] = len(body.split())
    r['pages_ff'] = body.count('\f') + 1
    # references
    seg = find_refs_segment(body)
    if seg is not None:
        n1, n2 = count_refs(seg)
        n = n1 if n1 else n2
        if n2 >= 5 and n > 2 * n2:  # block counting broke (numbered list, tables); fall back to author-year keys
            n = n2
        r['refs_n'] = n
        r['refs_n_alt'] = n2
        flat = re.sub(r'\s+', ' ', seg)
        tj = {k: len(re.findall(p, flat)) for k, p in TOP_JOURNALS.items()}
        r['refs_top_journal'] = sum(tj.values())
        r['refs_JF'] = tj['JF']; r['refs_JFE'] = tj['JFE']; r['refs_RFS'] = tj['RFS']
        r['refs_working_paper'] = len(re.findall(r'[Ww]orking [Pp]aper|\bNBER\b|\bSSRN\b|mimeo|unpublished', flat))
        r['refs_web_sources'] = len(re.findall(r'https?://|www\.|Retrieved from|Accessed', flat))
        r['refs_found'] = 1
    else:
        r['refs_n'] = r['refs_n_alt'] = r['refs_top_journal'] = r['refs_JF'] = r['refs_JFE'] = r['refs_RFS'] = r['refs_working_paper'] = r['refs_web_sources'] = ''
        r['refs_found'] = 0
    # intro
    intro = find_intro(body)
    if intro:
        r['intro_words'] = intro[0]
        it = intro[1]
        r['intro_has_question'] = int(bool(re.search(r'\?\s', it)))
        r['intro_rq_phrase'] = int(bool(re.search(RQ_PHRASE, it, re.I)))
        r['intro_results_preview'] = int(bool(re.search(r'we find|our (main )?results? (show|indicate|suggest)|our findings', it, re.I)))
        r['intro_contrib'] = int(bool(re.search(CONTRIB, it, re.I)))
        r['intro_numbers'] = len(re.findall(r'\d+\.\d+\s?(%|percent|basis points|bps)', it))
    else:
        r['intro_words'] = ''; r['intro_has_question'] = r['intro_rq_phrase'] = r['intro_results_preview'] = r['intro_contrib'] = r['intro_numbers'] = ''
    main = body[: int(len(body) * 0.85)]  # exclude trailing refs/appendix for prose counts
    r['rq_phrase_count'] = len(re.findall(RQ_PHRASE, main, re.I))
    r['anchor_phrases'] = len(re.findall(ANCHOR, main, re.I))
    r['contrib_phrases'] = len(re.findall(CONTRIB, main, re.I))
    r['null_language'] = len(re.findall(NULL_LANG, main, re.I))
    r['robustness_mentions'] = len(re.findall(ROBUST, main, re.I))
    r['placebo'] = int(bool(re.search(PLACEBO, main, re.I)))
    r['pretrend'] = int(bool(re.search(PRETREND, main, re.I)))
    r['swedish_mentions'] = len(re.findall(SWEDISH, main))
    r['nordic_mentions'] = len(re.findall(NORDIC, main))
    r['policy_mentions'] = len(re.findall(POLICY, main, re.I))
    r['qualitative_mentions'] = len(re.findall(QUAL, main, re.I))
    hyp = set(int(x) for x in re.findall(HYPO, main) if 0 < int(x) < 20)
    r['hypotheses_n'] = max(hyp) if hyp else 0
    tabs = [int(x) for x in re.findall(r'\bTable\s+(\d{1,2})\b', main)]
    figs = [int(x) for x in re.findall(r'\bFigure\s+(\d{1,2})\b', main)]
    r['tables_max'] = max(tabs) if tabs else 0
    r['figures_max'] = max(figs) if figs else 0
    r['t_stats'] = len(re.findall(r'\(\s?-?\d+\.\d+\s?\)|t\s?[=-]\s?-?\d+\.\d+|\*\*\*', main))
    r['has_toc'] = int(bool(re.search(r'^\s*(Table of )?Contents\s*$', body[:15000], re.M | re.I)))
    for k, p in METHODS.items():
        r['m_' + k] = len(re.findall(p, main, re.I))
    for k, p in SOURCES.items():
        r['src_' + k] = len(re.findall(p, main, re.I))
    r['cites_in_text'] = len(re.findall(r'\((?:[A-Z][A-Za-z\-\']+(?:,| and| &| et al\.?)?\s?){1,4}\s?,?\s?(?:19[5-9]|20[0-2])\d[a-z]?', main))
    return r


def main():
    args = sys.argv[1:]
    text_dir, out_csv = args[0], args[1]
    index = None; winners_md = None
    if '--index' in args:
        index = json.load(open(args[args.index('--index') + 1]))
    if '--winners' in args:
        winners_md = open(args[args.index('--winners') + 1]).read()
    meta = {}
    if index:
        for rec in index['records']:
            meta[str(rec.get('mediumid'))] = rec
    winner_ids = set(re.findall(r'MediumId=(\d+)', winners_md)) if winners_md else set()
    rows = []
    for fn in sorted(os.listdir(text_dir)):
        if not fn.endswith('.txt'):
            continue
        stem = fn[:-4]
        try:
            text = open(os.path.join(text_dir, fn), errors='ignore').read()
        except Exception as e:
            continue
        row = {'id': stem}
        m = meta.get(stem)
        if m:
            row['group'] = 'winner' if stem in winner_ids else 'non_winner'
            row['year'] = m.get('year'); row['title'] = m.get('title'); row['n_authors'] = len(m.get('authors') or [])
            row['pages_catalogue'] = (re.findall(r'\d+', m.get('pages') or '') or [''])[0]
            row['abstract_words'] = len((m.get('abstract') or '').split())
            row['title_has_colon'] = int(':' in (m.get('title') or '')); row['title_has_question'] = int('?' in (m.get('title') or ''))
        else:
            row['group'] = 'winner' if stem[:4].isdigit() else 'unknown'
            row['year'] = stem[:4] if stem[:4].isdigit() else ''
            row['title'] = stem; row['n_authors'] = ''; row['pages_catalogue'] = ''; row['abstract_words'] = ''; row['title_has_colon'] = ''; row['title_has_question'] = ''
        row.update(analyze(text))
        rows.append(row)
    if not rows:
        print('no rows'); return
    cols = list(rows[0].keys())
    for r0 in rows:
        for k in r0:
            if k not in cols: cols.append(k)
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print('wrote', len(rows), 'rows to', out_csv)


if __name__ == '__main__':
    main()
