#!/usr/bin/env python3
"""PCA of research architecture: 25 awarded SSE finance theses against 635 non-winners.
Usage: pca_winners.py <arch_all.csv> <winners_table.csv> <out_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

arch_csv, wtab_csv, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out + '/fig', exist_ok=True); dat = out + '/data'; os.makedirs(dat, exist_ok=True)
df = pd.read_csv(arch_csv)
df['year'] = df['id'].str[:4].where(df['group'] == 'winner', np.nan)

# non-winner year from catalogue index if available
idx = None
here = os.path.dirname(os.path.abspath(__file__))
for cand in [os.path.join(here, '..', '..', 'non_winners', 'catalogue_index.json'),
             os.path.join(os.path.dirname(os.path.abspath(arch_csv)), '..', '..', '..', 'non_winners', 'catalogue_index.json'),
             'non_winners/catalogue_index.json']:
    if os.path.exists(cand):
        idx = json.load(open(cand)); break
if idx:
    ymap = {str(r.get('mediumid')): r.get('year') for r in idx['records']}
    df.loc[df.group == 'non_winner', 'year'] = df.loc[df.group == 'non_winner', 'id'].map(ymap)
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# ---------- feature engineering ----------
def L(x): return np.log1p(pd.to_numeric(x, errors='coerce'))
F = pd.DataFrame(index=df.index)
# structure (shares of main text)
F['sh_intro'] = df.sh_intro
F['sh_frontlit'] = df.sh_background + df.sh_literature + df.sh_hypotheses
F['sh_design'] = df.sh_data + df.sh_method
F['sh_results'] = df.sh_results + df.sh_robustness
F['sh_discconcl'] = df.sh_discussion + df.sh_conclusion
F['n_sections'] = df.n_sections
F['sep_robustness'] = df.sep_robustness_section
F['sep_hypotheses'] = df.sep_hypotheses_section
F['sep_discussion'] = df.sep_discussion_section
F['sep_background'] = df.sep_background_section
# introduction
F['intro_words_log'] = L(df.intro_words)
F['intro_question'] = df.intro_question
F['intro_preview'] = df.intro_preview
F['intro_numbers'] = df.intro_numbers_per1k
F['intro_cites'] = df.intro_cites_per1k
F['intro_contrib'] = df.intro_contrib
F['intro_roadmap'] = df.intro_roadmap
F['intro_anchor'] = df.intro_anchor
# conclusion
F['concl_hedge'] = df.concl_hedge_per1k
F['concl_limit'] = df.concl_limit
F['concl_numbers'] = df.concl_numbers_per1k
F['concl_null'] = df.concl_null
# design / identification / inference language (per 1000 words)
F['anchor'] = df.anchor_per1k
F['contrib'] = df.contrib_per1k
F['null_lang'] = df.null_per1k
F['hedge'] = df.hedge_per1k
F['strong'] = df.strong_per1k
F['limit'] = df.limit_per1k
F['magnitude'] = df.magnitude_per1k
F['se_rigor'] = df.se_rigor_per1k
F['ident'] = df.ident_per1k
F['policy'] = df.policy_per1k
F['robust'] = df.robust_per1k
F['placebo'] = df.placebo
F['pretrend'] = df.pretrend
F['equations_log'] = L(df.n_equations)
F['hypotheses_n'] = df.hypotheses_n_capped
# output and writing
F['tables'] = df.tables_max
F['figures'] = df.figures_max
F['tstats'] = df.tstat_per1k
F['cites'] = df.cites_per1k
F['refs_log'] = L(df.refs_years)
F['refs_topj_share'] = df.refs_topj_share
F['refs_web_log'] = L(df.refs_web)
F['we'] = df.we_per1k
F['we_start'] = df.sent_we_start_share
F['sent_len'] = df.sent_len_mean
F['word_len'] = df.word_len_mean
F['words_log'] = L(df.words_total)
F['swedish'] = df.swedish_per1k
# method vocabulary
for m in ['did', 'event', 'rdd', 'iv', 'fe', 'famamacbeth', 'survey_qual', 'timeseries', 'ml']:
    F['m_' + m] = L(df['m_' + m])

F = F.apply(pd.to_numeric, errors='coerce')
# keep theses whose sections parsed (needed for shares)
ok = df.sections_ok == 1
F = F[ok].copy(); meta = df[ok].copy()
# winsorise at 1/99 pct and impute medians (computed on the full pooled sample)
lo, hi = F.quantile(0.01), F.quantile(0.99)
F = F.clip(lower=lo, upper=hi, axis=1)
F = F.fillna(F.median())
W = (meta.group == 'winner').values

LABELS = {
 'sh_intro': 'Andel introduktion', 'sh_frontlit': 'Andel bakgrund/litteratur/hypoteser', 'sh_design': 'Andel data+metod',
 'sh_results': 'Andel resultat+robusthet', 'sh_discconcl': 'Andel diskussion+slutsats', 'n_sections': 'Antal huvudavsnitt',
 'sep_robustness': 'Eget robusthetsavsnitt', 'sep_hypotheses': 'Eget hypotesavsnitt', 'sep_discussion': 'Eget diskussionsavsnitt', 'sep_background': 'Eget bakgrundsavsnitt',
 'intro_words_log': 'Intro-längd (log ord)', 'intro_question': 'Explicit fråga i intro', 'intro_preview': 'Resultat förhandsvisas i intro ("we find")',
 'intro_numbers': 'Siffror med %/bps i intro', 'intro_cites': 'Citeringar i intro /1k ord', 'intro_contrib': 'Bidragsformulering i intro',
 'intro_roadmap': 'Disposition i intro', 'intro_anchor': 'Ankarfraser i intro',
 'concl_hedge': 'Hedging-ord i slutsats /1k', 'concl_limit': 'Begränsningar nämnda i slutsats', 'concl_numbers': 'Siffror i slutsats /1k', 'concl_null': 'Nollresultatspråk i slutsats',
 'anchor': 'Ankarfraser ("we follow", "replicate") /1k', 'contrib': 'Bidragsfraser /1k', 'null_lang': 'Nollresultatspråk /1k', 'hedge': 'Hedging-ord /1k',
 'strong': 'Överdrivande ord ("prove", "clearly") /1k', 'limit': 'Begränsningsord /1k', 'magnitude': 'Ekonomisk storlek (bps, pp, "economically") /1k',
 'se_rigor': 'SE-rigor (clustered, Newey-West, robust) /1k', 'ident': 'Identifieringsvokabulär (DiD, treatment, placebo) /1k', 'policy': 'Reform/regel/tröskel-ord /1k',
 'robust': '"Robustness" /1k', 'placebo': 'Placebotest', 'pretrend': 'Parallella trender', 'equations_log': 'Numrerade ekvationer (log)', 'hypotheses_n': 'Antal numrerade hypoteser (tak 6)',
 'tables': 'Högsta tabellnummer', 'figures': 'Högsta figurnummer', 'tstats': 't-stat/stjärnor /1k', 'cites': 'Textciteringar /1k', 'refs_log': 'Referenslista (log antal)',
 'refs_topj_share': 'Andel toppjournaler i referenser', 'refs_web_log': 'Webbkällor (log)', 'we': '"we" /1k', 'we_start': 'Andel meningar som börjar med "We"',
 'sent_len': 'Meningslängd (ord)', 'word_len': 'Ordlängd', 'words_log': 'Total längd (log ord)', 'swedish': 'Svensk kontext /1k',
 'm_did': 'Vokabulär: DiD', 'm_event': 'Vokabulär: eventstudie', 'm_rdd': 'Vokabulär: RD', 'm_iv': 'Vokabulär: IV', 'm_fe': 'Vokabulär: fixed effects',
 'm_famamacbeth': 'Vokabulär: faktor/portföljsortering', 'm_survey_qual': 'Vokabulär: enkät/intervju/kvalitativ', 'm_timeseries': 'Vokabulär: GARCH/VAR', 'm_ml': 'Vokabulär: ML',
}

# ---------- A. per-feature contrast ----------
rows = []
Fw, Fn = F[W], F[~W]
recent = (meta.year >= 2018) & (meta.year <= 2024)
for c in F.columns:
    a, b = Fw[c], Fn[c]
    sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    d = (a.mean() - b.mean()) / sd if sd > 0 else 0
    try: p = stats.mannwhitneyu(a, b, alternative='two-sided').pvalue
    except Exception: p = np.nan
    ar, br = F[W & recent.values][c], F[~W & recent.values][c]
    try: pr = stats.mannwhitneyu(ar, br, alternative='two-sided').pvalue
    except Exception: pr = np.nan
    rows.append(dict(feature=c, label=LABELS.get(c, c), winners_median=a.median(), nonwinners_median=b.median(),
                     winners_mean=a.mean(), nonwinners_mean=b.mean(), cohen_d=d, p_mw=p,
                     winners_median_2018_24=ar.median(), nonwinners_median_2018_24=br.median(), p_mw_2018_24=pr,
                     sd_ratio=(a.std(ddof=1) / b.std(ddof=1)) if b.std(ddof=1) > 0 else np.nan))
contrast = pd.DataFrame(rows).sort_values('cohen_d', key=np.abs, ascending=False)
contrast.to_csv(dat + '/feature_contrast.csv', index=False)

# ---------- B. pooled PCA ----------
sc = StandardScaler().fit(F)
Z = sc.transform(F)
pca = PCA(n_components=10, random_state=0).fit(Z)
S = pca.transform(Z)
evr = pca.explained_variance_ratio_
load = pd.DataFrame(pca.components_.T, index=F.columns, columns=[f'PC{i+1}' for i in range(10)])
load.to_csv(dat + '/pooled_loadings.csv')
scores = pd.DataFrame(S, columns=load.columns, index=meta.index)
scores.insert(0, 'id', meta.id.values); scores.insert(1, 'group', meta.group.values); scores.insert(2, 'year', meta.year.values)
scores.to_csv(dat + '/pooled_scores.csv', index=False)
pc_contrast = []
for k in range(10):
    a, b = S[W, k], S[~W, k]
    sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    pc_contrast.append(dict(pc=f'PC{k+1}', var_explained=evr[k], winners_mean=a.mean(), nonwinners_mean=b.mean(),
                            cohen_d=(a.mean() - b.mean()) / sd, p_mw=stats.mannwhitneyu(a, b).pvalue,
                            winners_sd=a.std(ddof=1), nonwinners_sd=b.std(ddof=1)))
pc_contrast = pd.DataFrame(pc_contrast); pc_contrast.to_csv(dat + '/pooled_pc_contrast.csv', index=False)

# Fisher discriminant direction in the 10-PC space (winner-likeness), with leave-one-out AUC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import roc_auc_score
y = W.astype(int)
lda = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
prob = cross_val_predict(lda, S, y, cv=cv, method='decision_function')
auc_cv = roc_auc_score(y, prob)
lda.fit(S, y)
# direction in original standardised feature space
w_feat = pca.components_.T @ lda.coef_.ravel()
direction = pd.Series(w_feat, index=F.columns).sort_values(key=np.abs, ascending=False)
direction.to_csv(dat + '/winner_direction_feature_weights.csv', header=['weight'])
meta = meta.assign(winner_score=lda.decision_function(S), winner_score_cv=prob)
meta[['id', 'group', 'year', 'winner_score', 'winner_score_cv']].sort_values('winner_score_cv', ascending=False).to_csv(dat + '/winner_likeness_scores.csv', index=False)

# ---------- C. winners-only PCA ----------
ARCH = ['sh_intro', 'sh_frontlit', 'sh_design', 'sh_results', 'sh_discconcl', 'intro_words_log', 'intro_question', 'intro_preview', 'intro_numbers',
        'intro_cites', 'intro_contrib', 'anchor', 'null_lang', 'hedge', 'limit', 'magnitude', 'se_rigor', 'ident', 'policy', 'robust',
        'equations_log', 'hypotheses_n', 'tables', 'figures', 'tstats', 'cites', 'refs_log', 'refs_topj_share', 'we', 'sent_len', 'words_log']
Xw = Fw[ARCH]
Xw = Xw.loc[:, Xw.std() > 0]
scw = StandardScaler().fit(Xw); Zw = scw.transform(Xw)
pcaw = PCA(n_components=6, random_state=0).fit(Zw); Sw = pcaw.transform(Zw)
loadw = pd.DataFrame(pcaw.components_.T, index=Xw.columns, columns=[f'PC{i+1}' for i in range(6)])
loadw.to_csv(dat + '/winners_loadings.csv')
wmeta = meta[W].copy()
wmeta['short'] = wmeta.id.str[:4] + ' ' + wmeta.id.str.split('_').str[1].str[0].str.upper()  # 2011 P / 2011 S
for i in range(6): wmeta[f'PC{i+1}'] = Sw[:, i]
# archetypes: Ward clustering on first 4 PCs
Lk = linkage(Sw[:, :4], 'ward')
wmeta['cluster'] = fcluster(Lk, 3, 'maxclust')
# hand-coded design features from winners_table.csv
wt = pd.read_csv(wtab_csv)
wt['key'] = wt.year.astype(str) + ' ' + wt.prize.str[0]
wmeta = wmeta.merge(wt[['key', 'field', 'identification', 'anchor_paper', 'replicates_published_table', 'explicit_extension', 'result_direction', 'n_main_tables', 'n_figures', 'pages_main_text']], left_on='short', right_on='key', how='left')
wmeta.to_csv(dat + '/winners_scores_clusters.csv', index=False)
# supplementary correlations of coded variables with winner PCs
def code_ident(s):
    s = s.lower()
    if any(k in s for k in ['diff-in-diff', 'rd at', 'randomized', 'iv using', 'blp iv']): return 'kvasiexperiment'
    if 'event' in s and 'diff' not in s: return 'eventstudie'
    if any(k in s for k in ['fama-macbeth', 'spanning', 'nelson-siegel', 'conditional capm', 'fgls']): return 'asset pricing-test'
    if 'structural' in s: return 'strukturmodell'
    return 'panel/tvärsnittsregression'
wmeta['ident_class'] = wmeta.identification.fillna('').map(code_ident)
wmeta['replicates'] = wmeta.replicates_published_table.fillna('').str.lower().str.extract(r'^(yes|partly|no)')[0]
wmeta['result'] = wmeta.result_direction.fillna('').str.lower().map(lambda s: 'null' if s.startswith('null') else ('mixed' if 'mixed' in s else 'positive'))
wmeta[['id', 'short', 'cluster', 'PC1', 'PC2', 'PC3', 'ident_class', 'replicates', 'result', 'field']].to_csv(dat + '/winners_scores_clusters.csv', index=False)

# ---------- D. homogeneity: what winners share (low spread) vs where they differ ----------
hom = contrast[['feature', 'label', 'cohen_d', 'p_mw', 'sd_ratio', 'winners_median', 'nonwinners_median']].copy()
hom.to_csv(dat + '/homogeneity.csv', index=False)

# ---------- figures ----------
BLUE, ORANGE, GRAY, INK, MUTED, GRID, SURF = '#2a78d6', '#eb6834', '#c3c2b7', '#0b0b0b', '#898781', '#e1e0d9', '#fcfcfb'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': GRID, 'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': SURF, 'axes.facecolor': SURF})

def biplot_pooled(i, j, fn, title):
    fig, ax = plt.subplots(figsize=(8, 6.2))
    ax.scatter(S[~W, i], S[~W, j], s=10, c=GRAY, alpha=0.6, linewidths=0, label=f'Icke-vinnare (n={int((~W).sum())})')
    for prize, col, mk in [('per_hiller', BLUE, 'o'), ('staffan_viotti', ORANGE, 's')]:
        m = W & meta.id.str.contains(prize).values
        ax.scatter(S[m, i], S[m, j], s=55, c=col, marker=mk, edgecolors='white', linewidths=1.2,
                   label=('Per Hiller-pris' if prize == 'per_hiller' else 'Staffan Viotti-pris') + f' (n={int(m.sum())})')
        for k in np.where(m)[0]:
            ax.annotate(meta.id.iloc[k][:4], (S[k, i], S[k, j]), xytext=(4, 3), textcoords='offset points', fontsize=7, color=INK)
    ax.axhline(0, color=GRID, lw=0.8, zorder=0); ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    ax.set_xlabel(f'PC{i+1} ({evr[i]*100:.1f} % av variansen)'); ax.set_ylabel(f'PC{j+1} ({evr[j]*100:.1f} % av variansen)')
    ax.set_title(title, loc='left', color=INK, fontsize=11)
    ax.legend(frameon=False, loc='best', fontsize=8)
    fig.tight_layout(); fig.savefig(out + '/fig/' + fn, dpi=160); plt.close(fig)

biplot_pooled(0, 1, 'pooled_pc1_pc2.png', 'Poolad PCA: PC1 och PC2 (störst varians) skiljer inte vinnare från mängden')
# pick the two PCs that separate winners most
top2 = pc_contrast.sort_values('cohen_d', key=np.abs, ascending=False).pc.head(2).tolist()
ii, jj = int(top2[0][2:]) - 1, int(top2[1][2:]) - 1
biplot_pooled(min(ii, jj), max(ii, jj), 'pooled_best_separation.png', f'De två komponenter som skiljer vinnare mest ({top2[0]} och {top2[1]})')

# scree
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.bar(range(1, 11), evr * 100, color=BLUE, width=0.7)
ax.plot(range(1, 11), np.cumsum(evr) * 100, color=ORANGE, marker='o', ms=4)
ax.set_xlabel('Komponent'); ax.set_ylabel('% varians'); ax.set_title('Förklarad varians, poolad PCA (staplar) och kumulativ (linje)', loc='left', fontsize=10)
ax.grid(axis='y', color=GRID, lw=0.6); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(out + '/fig/scree_pooled.png', dpi=160); plt.close(fig)

# dumbbell of standardised differences (top 24 by |d|)
top = contrast.head(24).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 7.5))
cols = [BLUE if d > 0 else ORANGE for d in top.cohen_d]
ax.barh(top.label, top.cohen_d, color=cols, height=0.6)
for yv, (d, p) in enumerate(zip(top.cohen_d, top.p_mw)):
    ax.text(d + (0.03 if d > 0 else -0.03), yv, ('p<0.01' if p < 0.01 else f'p={p:.2f}'), va='center', ha='left' if d > 0 else 'right', fontsize=7, color=MUTED)
ax.axvline(0, color=GRID); ax.set_xlabel("Cohen's d (vinnare minus icke-vinnare, standardiserat)")
ax.set_title('Var vinnarna avviker från de 635 icke-vinnarna (24 största effekterna)', loc='left', fontsize=10)
ax.grid(axis='x', color=GRID, lw=0.6); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(out + '/fig/feature_contrast.png', dpi=160); plt.close(fig)

# winners-only biplot
fig, ax = plt.subplots(figsize=(8.5, 7))
CL = {1: BLUE, 2: ORANGE, 3: '#1baf7a'}
for cl in sorted(wmeta.cluster.unique()):
    m = wmeta.cluster == cl
    ax.scatter(wmeta.PC1[m], wmeta.PC2[m], s=70, c=CL[cl], edgecolors='white', linewidths=1.2, label=f'Kluster {cl} (n={int(m.sum())})')
for _, r in wmeta.iterrows():
    ax.annotate(r.short, (r.PC1, r.PC2), xytext=(5, 3), textcoords='offset points', fontsize=7.5, color=INK)
# loading arrows for the 12 largest loadings
sc_ = 2.6
mag = (loadw.PC1 ** 2 + loadw.PC2 ** 2).sort_values(ascending=False).head(12).index
for f in mag:
    ax.annotate('', xy=(loadw.PC1[f] * sc_ * 2, loadw.PC2[f] * sc_ * 2), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.9))
    ax.text(loadw.PC1[f] * sc_ * 2.15, loadw.PC2[f] * sc_ * 2.15, LABELS.get(f, f).split(' (')[0], fontsize=6.5, color=MUTED, ha='center')
ax.axhline(0, color=GRID, lw=0.8, zorder=0); ax.axvline(0, color=GRID, lw=0.8, zorder=0)
ev = pcaw.explained_variance_ratio_
ax.set_xlabel(f'PC1 ({ev[0]*100:.1f} %)'); ax.set_ylabel(f'PC2 ({ev[1]*100:.1f} %)')
ax.set_title('PCA på enbart de 25 vinnarna: P = Per Hiller-pris, S = Staffan Viotti-pris', loc='left', fontsize=11)
ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(out + '/fig/winners_pca.png', dpi=160); plt.close(fig)

# loadings heatmap (winners PCA, 4 PCs)
fig, ax = plt.subplots(figsize=(6, 8.5))
Lh = loadw.iloc[:, :4]
im = ax.imshow(Lh.values, cmap='RdBu_r', vmin=-0.5, vmax=0.5, aspect='auto')
ax.set_yticks(range(len(Lh))); ax.set_yticklabels([LABELS.get(f, f) for f in Lh.index], fontsize=7.5)
ax.set_xticks(range(4)); ax.set_xticklabels([f'PC{i+1}\n{ev[i]*100:.0f} %' for i in range(4)], fontsize=8)
for (yi, xi), v in np.ndenumerate(Lh.values):
    if abs(v) >= 0.2: ax.text(xi, yi, f'{v:+.2f}', ha='center', va='center', fontsize=6.5, color='white' if abs(v) > 0.35 else INK)
ax.set_title('Laddningar, vinnar-PCA', loc='left', fontsize=10)
fig.colorbar(im, ax=ax, shrink=0.4, label='laddning')
fig.tight_layout(); fig.savefig(out + '/fig/winners_loadings.png', dpi=160); plt.close(fig)

# ---------- print summary ----------
pd.set_option('display.width', 200); pd.set_option('display.max_rows', 200)
print('N used:', len(F), 'winners', int(W.sum()))
print('\n=== pooled PCA variance explained:', np.round(evr * 100, 1), 'cum', np.round(np.cumsum(evr) * 100, 1))
print('\n=== PC contrast winners vs non-winners'); print(pc_contrast.round(3).to_string())
for k in range(5):
    print(f'\n--- PC{k+1} top loadings'); print(load[f'PC{k+1}'].sort_values(key=np.abs, ascending=False).head(10).round(2).to_string())
print('\n=== LDA winner-likeness, 5-fold CV AUC =', round(auc_cv, 3))
print(direction.head(20).round(2).to_string())
print('\n=== feature contrast (top 30 by |d|)'); print(contrast.head(30)[['label', 'winners_median', 'nonwinners_median', 'cohen_d', 'p_mw', 'p_mw_2018_24', 'sd_ratio']].round(3).to_string())
print('\n=== homogeneity: lowest sd_ratio (winners tighter than population)'); print(contrast.sort_values('sd_ratio').head(15)[['label', 'sd_ratio', 'cohen_d', 'winners_median', 'nonwinners_median']].round(3).to_string())
print('\n=== highest sd_ratio (free parameters)'); print(contrast.sort_values('sd_ratio', ascending=False).head(10)[['label', 'sd_ratio', 'cohen_d']].round(3).to_string())
print('\n=== winners PCA variance:', np.round(ev * 100, 1))
for k in range(4):
    print(f'\n--- winners PC{k+1} loadings'); print(loadw[f'PC{k+1}'].sort_values(key=np.abs, ascending=False).head(8).round(2).to_string())
print('\n=== clusters'); print(wmeta[['short', 'cluster', 'PC1', 'PC2', 'ident_class', 'replicates', 'result', 'field']].sort_values(['cluster', 'PC1']).round(2).to_string())
print('\n=== cluster x ident'); print(pd.crosstab(wmeta.cluster, wmeta.ident_class)); print(pd.crosstab(wmeta.cluster, wmeta.replicates)); print(pd.crosstab(wmeta.cluster, wmeta.result))
print('\n=== winner-likeness: rank of each winner among all (1=most winner-like)')
rk = meta.winner_score_cv.rank(ascending=False)
print(pd.DataFrame({'id': meta.id[W].str[:45], 'rank': rk[W].astype(int)}).sort_values('rank').to_string())
print('\n=== top 15 non-winners by winner-likeness'); print(meta[~W].sort_values('winner_score_cv', ascending=False).head(15)[['id', 'year', 'winner_score_cv']].round(2).to_string())
