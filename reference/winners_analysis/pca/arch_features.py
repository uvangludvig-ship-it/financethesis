#!/usr/bin/env python3
"""Research-architecture features for SSE theses (pdftotext -layout output).
Usage: arch_features.py <out_csv> <text_dir> [<text_dir> ...]
"""
import csv, os, re, sys, unicodedata

CAT_KEYS = [
 ('references', r'\b(references?|reference list|bibliography|works cited|literature list|list of references|sources)\b'),
 ('appendix',   r'\bappendi(x|ces)\b'),
 ('intro',      r'\bintroduction\b'),
 ('conclusion', r'\bconclu'),
 ('discussion', r'\bdiscussion|implications|interpretation|limitations|further research|future research'),
 ('robustness', r'\brobust|sensitivity|alternative specification|additional tests|further tests'),
 ('results',    r'\bresults?\b|\bfindings\b|empirical (analysis|evidence|results)|\banalysis\b|\bevidence\b'),
 ('hypotheses', r'hypothes|predictions|propositions'),
 ('method',     r'method|empirical (strategy|approach|framework|design|model|specification)|research design|identification|estimation|econometric|model specification|\bmodels?\b|\bapproach\b|\bspecification\b|\bprocedure\b|regression design'),
 ('data',       r'\bdata\b|\bsample\b|descriptive statistics|summary statistics|\bvariables?\b|data description'),
 ('literature', r'literature|previous (research|studies|work|literature)|prior (research|literature|studies)|related (research|work|literature|studies)|theor|empirical research|existing research|earlier (research|studies)|academic research|review'),
 ('background', r'background|institutional|setting|history|overview|context|\bmarket\b|regulat|\bthe (swedish|norwegian|french|us|european)\b|adoption of|\bframework\b|definitions?'),
]
CAT_RE = [(k, re.compile(p, re.I)) for k, p in CAT_KEYS]

NUM_HEAD = re.compile(r'^\s{0,40}(?:(\d{1,2})|([IVX]{1,4}))[\.\)]?\s{1,4}([A-Z][A-Za-z][A-Za-z0-9 ,:;&\-\'’?()/]{1,90}?)\s*$')
NUM_HEAD2 = re.compile(r'^\s{0,40}(?:(\d{1,2})|([IVX]{1,4}))[\.\)]?\s{1,4}([A-Z][A-Za-z][A-Za-z ,:;&\-\'’?()/]{1,60}?)\s{4,}\S')
GENERIC_HEAD = re.compile(r'^\s{0,40}([A-Z][A-Za-z][A-Za-z ,:&\-\'’]{2,60})\s*$')
BARE_HEAD = re.compile(r'^\s{0,40}((?:\d{1,2}\.?\s+)?(?:Introduction|INTRODUCTION|Background|BACKGROUND|Literature Review|LITERATURE REVIEW|Previous Research|PREVIOUS RESEARCH|Theoretical Framework|THEORETICAL FRAMEWORK|Hypotheses|HYPOTHESES|Data|DATA|Methodology|METHODOLOGY|Method|METHOD|Data and Methodology|DATA AND METHODOLOGY|Empirical Results|EMPIRICAL RESULTS|Results|RESULTS|Robustness|ROBUSTNESS|Discussion|DISCUSSION|Conclusion|CONCLUSION|Conclusions|CONCLUSIONS|Concluding Remarks|CONCLUDING REMARKS|References|REFERENCES|Reference List|REFERENCE LIST|Bibliography|BIBLIOGRAPHY|Appendix|APPENDIX|Appendices|APPENDICES)(?:[A-Za-z ,:&\-]{0,60})?)\s*$')

ANCHOR = r"we follow|following the (methodology|approach|method|framework|procedure|specification)|replicat|akin to|closely (follow|mimic|resembl)|based on the (methodology|approach|model|framework|specification) of|in line with the (methodology|approach) of|we adopt the (methodology|approach|method|specification)|we (employ|use|apply) the (same|methodology|approach|method)|methodology (of|used by|developed by|proposed by)|as in [A-Z][a-z]+ (and|&|et al)"
CONTRIB = r'to (our|the best of our) knowledge|first (study|paper|thesis) to|contribut(e|es|ion) to the literature|we contribute|fill(s)? (a|this) gap'
NULL_LANG = r'no (statistically |economically )?significant|not (statistically |economically )?significant|insignificant|fail(s|ed)? to reject|no evidence|cannot reject the null|do(es)? not find'
HEDGE = r'\b(may|might|could|possibly|perhaps|tendency|tendencies|weakly|somewhat|seems? to|appears? to|indicative)\b'
STRONG = r'\b(prove[sd]?|proof|clearly|undoubtedly|confirms?|definitely|strongly supports?)\b'
LIMIT = r'\blimitation|caveat|shortcoming|drawback|we acknowledge'
MAGN = r'economic(ally)? (significan|meaningful|magnitude)|basis points|\bbps\b|percentage points|standard deviation increase|one[- ]standard[- ]deviation'
SE_RIG = r'cluster(ed|ing)? (standard errors|at the|by)|newey[- ]west|heteroskedasticity|heteroscedasticity|robust standard errors|white standard errors|bootstrap'
IDENT = r'difference[- ]in[- ]difference|diff[- ]in[- ]diff|\bDiD\b|regression discontinuity|instrumental variable|\b2SLS\b|natural experiment|quasi[- ](natural )?experiment|treatment group|control group|treated (firms|stocks|funds|group)|exogenous (shock|variation)|parallel[- ]trend|pre[- ]trend|placebo'
POLICY = r'\breform\b|regulation|natural experiment|quasi[- ](natural )?experiment|policy change|exogenous (shock|variation)|\bdirective\b|new law|introduction of the (law|tax|rule|regulation)|\bban\b|\bquota\b|threshold|cutoff|cut-off'
TOPJ = r'Journal of Finance\b|Journal of Financial Economics|Review of Financial Studies|Quarterly Journal of Economics|American Economic Review|Journal of Political Economy|\bEconometrica\b|Review of Economic Studies|Journal of Financial and Quantitative Analysis|Review of Finance\b'
CITE = r'\((?:[A-Z][A-Za-z\-\']+(?:,| and| &| et al\.?)?\s?){1,4}\s?,?\s?(?:19[5-9]|20[0-2])\d[a-z]?'
EQN = re.compile(r'\(\s?\d{1,2}\s?\)\s*$', re.M)
ROADMAP = r'(remainder|rest) of (this|the) (paper|thesis|study) (is|proceeds)|is (structured|organi[sz]ed) as follows|section \d (describes|presents|discusses|introduces|outlines|concludes)'

SPACED = re.compile(r'^(\s*)((?:[A-Z&\-,:]{1,2}\s){5,}[A-Z&\-,:]{0,2})\s*$')
KW = ['INTRODUCTION','THEORETICAL','FRAMEWORK','PREVIOUS','RESEARCH','LITERATURE','REVIEW','METHODOLOGY','METHOD','DATA','RESULTS','DISCUSSION','CONCLUSIONS','CONCLUSION','BIBLIOGRAPHY','REFERENCES','APPENDIX','BACKGROUND','HYPOTHESES','ROBUSTNESS','ANALYSIS','EMPIRICAL','ABSTRACT','CONTENTS','ACKNOWLEDGEMENTS']
def norm(t):
    t = t.replace('\r', '')
    t = unicodedata.normalize('NFKC', t)
    t = t.replace(' ', ' ')
    out = []
    for ln in t.split('\n'):
        m = SPACED.match(ln)
        if m:
            body = m.group(2).replace(' ', '')
            for kw in KW:
                body = body.replace(kw, ' ' + kw + ' ')
            ln = m.group(1) + re.sub(r'\s+', ' ', body).strip()
        out.append(ln)
    return '\n'.join(out)

ROMAN = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12}
def headnum(h):
    n = h[2]
    if n is None: return None
    if n.isdigit(): return int(n)
    return ROMAN.get(n)

# manual category overrides for winners where the parser misreads the architecture (checked by eye)
OVERRIDE = {
 '2015_per_hiller_fund_flow_risk_and_cross_sectional_asset_prices': {'Hypotheses': 'results'},
 '2020_per_hiller_chasing_your_own_tail': {'LETF Rebalancing and the Market': 'results', 'Flow-Induced Market Impact of LETFs': 'results', 'Price Impact and Market Microstructure Invariance': 'results'},
 '2022_per_hiller_predicting_liquidity_in_cryptocurrency_market': {'Data limitations': 'data'},
 '2021_staffan_viotti_market_microstructure_invariance': {'Fundamental': 'background'},
 '2016_per_hiller_intermediary_asset_pricing_and_swedish_equity_market': {'Research question': 'intro'},
 '2011_staffan_viotti_impact_of_short_sale_bans': {'Impact on the Stock Market': 'literature'},
}
CUR_ID = [None]

def classify(title):
    for k, rx in CAT_RE:
        if rx.search(title):
            return k
    return 'other'

def find_headings(text):
    lines = text.split('\n')
    heads = []  # (line_idx, char_off, number, title, cat)
    off = 0
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        m = NUM_HEAD.match(s)
        title = None; num = None
        if m and not re.search(r'\d\s*$', s) and '....' not in s:
            num = m.group(1) or m.group(2); title = m.group(3).strip()
            # exclude things like "1 Introduction 3" (TOC) handled by trailing-digit; exclude table lines
            if re.match(r'(Table|Figure|Panel|Note|Source|Column|Model|Year|Month|Day|Mean|Std)', title):
                title = None
        else:
            m2 = BARE_HEAD.match(s)
            m3 = NUM_HEAD2.match(s)
            if m2 and '....' not in s and not re.search(r'\d\s*$', s):
                title = m2.group(1).strip()
                nm = re.match(r'(\d{1,2})\.?\s+(.*)', title)
                if nm: num = nm.group(1); title = nm.group(2)
            elif m3 and '....' not in s and classify(m3.group(3).strip()) != 'other':
                num = m3.group(1) or m3.group(2); title = m3.group(3).strip()
            else:
                m4 = GENERIC_HEAD.match(s)
                if m4 and len(m4.group(1).split()) <= 8:
                    prev_blank = (i == 0) or (not lines[i-1].strip())
                    cat = classify(m4.group(1))
                    if prev_blank and cat not in ('other', 'background', 'data', 'method', 'results'):
                        title = m4.group(1).strip(); num = None
                        heads.append([i, off, None, title, cat, 'generic'])
                        title = None
        if title and len(title.split()) <= 12:
            cat = classify(title)
            ov = OVERRIDE.get(CUR_ID[0], {})
            for k, v in ov.items():
                if k.lower() in title.lower(): cat = v
            heads.append([i, off, num, title, cat])
        off += len(ln) + 1
    return heads, lines

def section_shares(text):
    heads, lines = find_headings(text)
    n_lines = len(lines)
    # drop heads in first 8% of lines that look like TOC region: keep the LAST occurrence of 'intro' as start of body if there are several before 15% of doc
    intro_idx = [h for h in heads if h[4] == 'intro']
    if not intro_idx:
        return None
    # body start: the intro heading followed by >= 150 words before next heading candidate
    start_h = None
    for h in intro_idx:
        j = heads.index(h)
        nxt = heads[j+1][0] if j+1 < len(heads) else n_lines
        words = sum(len(l.split()) for l in lines[h[0]+1:nxt])
        if words >= 150:
            start_h = j; break
    if start_h is None:
        return None
    body_heads = heads[start_h:]
    # keep only top-level numbered headings if numbering exists; sequence must be increasing
    numbered = [h for h in body_heads if headnum(h) is not None and len(h) == 5]
    seq = []
    if len(numbered) >= 3:
        last = 0
        for h in numbered:
            n = headnum(h)
            if n == last + 1 or (n > last and n <= last + 2):
                if n == last + 2:
                    # try to recover the skipped top-level heading from its first "k.1" subsection
                    k = last + 1
                    sub = re.compile(r'^\s{0,40}' + str(k) + r'\.1\.?\s+([A-Z][A-Za-z ,&\-]{2,70})\s*$')
                    prev_line = seq[-1][0] if seq else 0
                    for li in range(prev_line + 1, h[0]):
                        ms = sub.match(lines[li])
                        if ms:
                            t = ms.group(1).strip(); c = classify(t)
                            for kk, v in OVERRIDE.get(CUR_ID[0], {}).items():
                                if kk.lower() in t.lower(): c = v
                            seq.append([li, 0, str(k), t, c]); break
                seq.append(h); last = n
            elif n == 1 and not seq:
                seq.append(h); last = 1
        if len(seq) < 3 or sum(1 for h in seq if h[4] != 'other') < 2:
            seq = []
        else:
            # a bare 'Introduction' before the numbered list (numbering starts after the intro)
            if seq[0][4] != 'intro':
                pre = [h for h in body_heads if h[4] == 'intro' and h[0] < seq[0][0]]
                if pre: seq.insert(0, pre[-1])
    if not seq:
        # fall back on bare headings of distinct category (first occurrence per category after intro)
        seen = set(); seq = []
        for h in body_heads:
            if h[4] in ('other',): continue
            if h[4] in seen and h[4] not in ('results',): continue
            seen.add(h[4]); seq.append(h[:5])
    # stop at references/appendix
    end_line = n_lines
    out = []
    for j, h in enumerate(seq):
        if h[4] in ('references', 'appendix'):
            end_line = h[0]; break
        nxt = seq[j+1][0] if j+1 < len(seq) else n_lines
        out.append((h[4], h[3], h[0], nxt))
    # also cut at any references heading anywhere after last section
    refs_any = [h for h in heads if h[4] == 'references' and h[0] > seq[0][0]]
    if refs_any:
        end_line = min(end_line, refs_any[0][0])
    secs = []
    for cat, title, a, b in out:
        b = min(b, end_line)
        if b <= a: continue
        w = sum(len(l.split()) for l in lines[a+1:b])
        secs.append((cat, title, w, a, b))
    total = sum(s[2] for s in secs)
    if total < 2000:
        return None
    return secs, total, lines, end_line

def analyze(path):
    CUR_ID[0] = os.path.basename(path)[:-4]
    text = norm(open(path, errors='ignore').read())
    r = {}
    words = text.split()
    r['words_total'] = len(words)
    ss = section_shares(text)
    cats = ['intro','background','literature','hypotheses','data','method','results','robustness','discussion','conclusion','other']
    for c in cats: r['sh_'+c] = ''
    if ss:
        secs, total, lines, end_line = ss
        shares = {c: 0.0 for c in cats}
        for cat, title, w, a, b in secs:
            # split combined data/method or results/discussion headings
            tl = title.lower()
            if cat in ('data','method') and re.search(r'data', tl) and re.search(r'method|empirical|design|approach', tl):
                shares['data'] += w/2; shares['method'] += w/2
            elif cat in ('results','discussion') and re.search(r'result|finding', tl) and re.search(r'discussion|analysis', tl):
                shares['results'] += w/2; shares['discussion'] += w/2
            elif cat in ('discussion','conclusion') and re.search(r'conclu', tl) and re.search(r'discussion|implication', tl):
                shares['discussion'] += w/2; shares['conclusion'] += w/2
            else:
                shares[cat] += w
        for c in cats: r['sh_'+c] = round(shares[c]/total, 4)
        r['n_sections'] = len(secs)
        r['main_words'] = total
        r['sep_lit_section'] = int(shares['literature'] > 0)
        r['sep_background_section'] = int(shares['background'] > 0)
        r['sep_hypotheses_section'] = int(shares['hypotheses'] > 0)
        r['sep_robustness_section'] = int(shares['robustness'] > 0)
        r['sep_discussion_section'] = int(shares['discussion'] > 0)
        r['sep_data_section'] = int(shares['data'] > 0)
        r['front_share'] = round((shares['intro']+shares['background']+shares['literature']+shares['hypotheses'])/total, 4)
        r['empirics_share'] = round((shares['data']+shares['method']+shares['results']+shares['robustness'])/total, 4)
        r['sections_ok'] = 1
        intro_sec = [s for s in secs if s[0]=='intro']
        intro_txt = '\n'.join(lines[intro_sec[0][3]+1:intro_sec[0][4]]) if intro_sec else ''
        concl_secs = [s for s in secs if s[0] in ('conclusion','discussion')]
        concl_txt = '\n'.join('\n'.join(lines[s[3]+1:s[4]]) for s in concl_secs)
        main_txt = '\n'.join(lines[secs[0][3]:end_line])
    else:
        r['n_sections'] = ''; r['main_words'] = ''
        for k in ['sep_lit_section','sep_background_section','sep_hypotheses_section','sep_robustness_section','sep_discussion_section','sep_data_section','front_share','empirics_share']:
            r[k] = ''
        r['sections_ok'] = 0
        intro_txt = ''; concl_txt = ''
        main_txt = text[: int(len(text)*0.85)]
    mw = max(len(main_txt.split()), 1)
    r['intro_words'] = len(intro_txt.split()) if intro_txt else ''
    if intro_txt:
        iw = max(len(intro_txt.split()),1)
        r['intro_question'] = int(bool(re.search(r'\?\s', intro_txt)))
        r['intro_rq_phrase'] = int(bool(re.search(r'research question', intro_txt, re.I)))
        r['intro_preview'] = int(bool(re.search(r'we (find|document|show|estimate)|our (main )?(results?|findings?) (show|indicate|suggest|are)', intro_txt, re.I)))
        r['intro_numbers_per1k'] = round(1000*len(re.findall(r'\d+(\.\d+)?\s?(%|percent|basis points|bps|percentage points|million|billion)', intro_txt, re.I))/iw, 2)
        r['intro_cites_per1k'] = round(1000*len(re.findall(CITE, intro_txt))/iw, 2)
        r['intro_contrib'] = int(bool(re.search(CONTRIB, intro_txt, re.I)))
        r['intro_roadmap'] = int(bool(re.search(ROADMAP, intro_txt, re.I)))
        r['intro_anchor'] = len(re.findall(ANCHOR, intro_txt, re.I))
        r['intro_share'] = r['sh_intro']
    else:
        for k in ['intro_question','intro_rq_phrase','intro_preview','intro_numbers_per1k','intro_cites_per1k','intro_contrib','intro_roadmap','intro_anchor','intro_share']:
            r[k] = ''
    if concl_txt:
        cw = max(len(concl_txt.split()),1)
        r['concl_words'] = cw
        r['concl_hedge_per1k'] = round(1000*len(re.findall(HEDGE, concl_txt, re.I))/cw, 2)
        r['concl_strong_per1k'] = round(1000*len(re.findall(STRONG, concl_txt, re.I))/cw, 2)
        r['concl_limit'] = len(re.findall(LIMIT, concl_txt, re.I))
        r['concl_numbers_per1k'] = round(1000*len(re.findall(r'\d+(\.\d+)?\s?(%|percent|basis points|bps|percentage points)', concl_txt, re.I))/cw, 2)
        r['concl_null'] = len(re.findall(NULL_LANG, concl_txt, re.I))
        r['concl_cites_per1k'] = round(1000*len(re.findall(CITE, concl_txt))/cw, 2)
    else:
        for k in ['concl_words','concl_hedge_per1k','concl_strong_per1k','concl_limit','concl_numbers_per1k','concl_null','concl_cites_per1k']:
            r[k] = ''
    # whole-main-text densities per 1000 words
    def d(p, flags=re.I): return round(1000*len(re.findall(p, main_txt, flags))/mw, 3)
    r['anchor_per1k'] = d(ANCHOR)
    r['contrib_per1k'] = d(CONTRIB)
    r['null_per1k'] = d(NULL_LANG)
    r['hedge_per1k'] = d(HEDGE)
    r['strong_per1k'] = d(STRONG)
    r['limit_per1k'] = d(LIMIT)
    r['magnitude_per1k'] = d(MAGN)
    r['se_rigor_per1k'] = d(SE_RIG)
    r['ident_per1k'] = d(IDENT)
    r['policy_per1k'] = d(POLICY)
    r['robust_per1k'] = d(r'robustness|robust to')
    r['placebo'] = int(bool(re.search(r'placebo', main_txt, re.I)))
    r['pretrend'] = int(bool(re.search(r'parallel[- ]trend|pre[- ]trend|common trend', main_txt, re.I)))
    r['cites_per1k'] = d(CITE, 0)
    r['we_per1k'] = d(r'\bwe\b')
    r['tstat_per1k'] = d(r'\(\s?-?\d+\.\d+\s?\)|t\s?[=-]\s?-?\d+\.\d+|\*\*\*', 0)
    r['n_equations'] = len(EQN.findall(main_txt))
    tabs = [int(x) for x in re.findall(r'\bTable\s+(\d{1,2})\b', main_txt)]
    figs = [int(x) for x in re.findall(r'\bFigure\s+(\d{1,2})\b', main_txt)]
    r['tables_max'] = max(tabs) if tabs else 0
    r['figures_max'] = max(figs) if figs else 0
    hyp = set(int(x) for x in re.findall(r'\b(?:H|Hypothesis\s*)(\d{1,2})\b', main_txt) if 0 < int(x) < 20)
    r['hypotheses_n'] = max(hyp) if hyp else 0
    r['hypotheses_n_capped'] = min(r['hypotheses_n'], 6)
    # methods vocab
    r['m_did'] = d(r'difference[- ]in[- ]difference|diff[- ]in[- ]diff|\bDiD\b')
    r['m_event'] = d(r'event[- ]stud|abnormal return')
    r['m_rdd'] = d(r'regression discontinuity')
    r['m_iv'] = d(r'instrumental variable|\b2SLS\b|two[- ]stage')
    r['m_fe'] = d(r'fixed[- ]effects?')
    r['m_famamacbeth'] = d(r'Fama[- ]?MacBeth|factor (model|loading)|portfolio sort|decile|quintile')
    r['m_survey_qual'] = d(r'\bsurvey\b|questionnaire|\binterview|qualitative|thematic')
    r['m_timeseries'] = d(r'\bGARCH\b|\bVAR\b|vector autoregress|cointegrat|unit root|ARIMA')
    r['m_ml'] = d(r'machine learning|neural network|random forest|\bLASSO\b|gradient boost')
    # sentence stats on prose (main text w/o table-ish lines)
    prose = '\n'.join(l for l in main_txt.split('\n') if len(l.split()) >= 6 and not re.search(r'\d\s+\d\s+\d', l))
    sents = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', prose) if len(s.split()) >= 3]
    if sents:
        lens = [len(s.split()) for s in sents]
        r['sent_len_mean'] = round(sum(lens)/len(lens), 2)
        r['sent_len_sd'] = round((sum((x-sum(lens)/len(lens))**2 for x in lens)/len(lens))**0.5, 2)
        r['sent_we_start_share'] = round(sum(1 for s in sents if re.match(r'\s*We\b', s))/len(sents), 4)
        wl = [len(w) for w in prose.split() if w.isalpha()]
        r['word_len_mean'] = round(sum(wl)/max(len(wl),1), 3)
    else:
        r['sent_len_mean'] = r['sent_len_sd'] = r['sent_we_start_share'] = r['word_len_mean'] = ''
    # references
    refs_m = list(re.finditer(r'^\s{0,40}(?:\d{1,2}\.?\s+)?(References|REFERENCES|Reference List|Reference list|REFERENCE LIST|Bibliography|BIBLIOGRAPHY|Works Cited|List of References|List of references)\s*:?\s*$', text, re.M))
    if refs_m:
        seg = text[refs_m[-1].end(): refs_m[-1].end()+70000]
        appx = re.search(r'^\s{0,40}(?:\d{1,2}\.?\s+)?Appendi', seg, re.M)
        if appx and appx.start() > 500: seg = seg[:appx.start()]
        years = re.findall(r'\b(19[5-9]\d|20[0-2]\d)[a-z]?\b', seg)
        r['refs_years'] = len(years)
        r['refs_topj'] = len(re.findall(TOPJ, seg))
        r['refs_topj_share'] = round(r['refs_topj']/max(r['refs_years'],1), 3)
        r['refs_web'] = len(re.findall(r'https?://|www\.|Retrieved|Accessed', seg))
        r['refs_wp'] = len(re.findall(r'[Ww]orking [Pp]aper|\bNBER\b|\bSSRN\b|mimeo|unpublished', seg))
        yrs = [int(y) for y in years if 1950 <= int(y) <= 2026]
        r['refs_median_year'] = sorted(yrs)[len(yrs)//2] if yrs else ''
    else:
        r['refs_years'] = r['refs_topj'] = r['refs_topj_share'] = r['refs_web'] = r['refs_wp'] = r['refs_median_year'] = ''
    r['abstract_words'] = ''
    am = re.search(r'\bAbstract\s*:?\s*\n(.{200,3500}?)\n\s*\n', text[:12000], re.S | re.I)
    if am: r['abstract_words'] = len(am.group(1).split())
    r['swedish_per1k'] = d(r'\bSweden\b|\bSwedish\b|\bStockholm\b|\bOMX|\bSEK\b|Nasdaq Stockholm|Riksbank', 0)
    return r

def main():
    out_csv = sys.argv[1]
    rows = []
    for td in sys.argv[2:]:
        grp = 'winner' if 'old_winners' in td else 'non_winner'
        for fn in sorted(os.listdir(td)):
            if not fn.endswith('.txt'): continue
            row = {'id': fn[:-4], 'group': grp}
            try:
                row.update(analyze(os.path.join(td, fn)))
            except Exception as e:
                row['error'] = repr(e)
            rows.append(row)
    cols = []
    for r0 in rows:
        for k in r0:
            if k not in cols: cols.append(k)
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print('wrote', len(rows), out_csv)

if __name__ == '__main__':
    main()
