import csv, json, collections, sys

import os
# Paths are relative to the repo root (financethesis).
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'
SRC_LOSERS = REPO + '/data/measurements/agentA_task1_round_membership.csv'
SRC_PANEL = REPO + '/data/panel/ppm_panel_2018_2026.csv'

losers = [r for r in csv.DictReader(open(SRC_LOSERS, encoding='utf-8')) if r['role'] == 'loser']
last = {}
for r in csv.DictReader(open(SRC_PANEL, encoding='utf-8')):
    last[r['fondnr']] = r

# ---------------------------------------------------------------------------
# Fund-level findings, keyed by fondnr.
# status: YES / NO / UNKNOWN  (status at the fund's PPM exit date, or current status if not yet exited)
# verification: VERIFIED (read from fondbestammelser / prospectus / annual report / company notice of approved rule change),
#               SECONDARY (company web page, news, or inference from a complete list of rule changes), UNKNOWN
# ---------------------------------------------------------------------------
U = 'UNKNOWN'
F = {}
def add(fondnr, company, domicile, status, since, maxf, applied, evdate, url, verif, note):
    F[str(fondnr)] = dict(fund_company=company, domicile=domicile, swing_status=status, swing_since=since,
                          max_factor_pct=maxf, applied_disclosed=applied, evidence_doc_date=evdate,
                          source_url=url, verification=verif, notes=note)

SEB_URL = 'https://sebgroup.com/sv/asset-management/nyheter-asset-management/2025/mojlighet-till-justerat-fondandelsvarde-infors-i-ett-antal-fonder'
SEB18 = 'https://sebgroup.com/globalassets/global-blocks/asset-management/news/fonders-nyheter-bilagor-och-new-list-block/kundunderrattelse-18.pdf'
STB = 'https://www.storebrandfonder.se/globalassets/dokument/redogorelser/kundbrev-forandringar-fondbestammelser-250515.pdf'
LAN_MC = 'https://cms-media.lannebo.se/sv/fonder/informationsbroschyr-lannebo-sweden-micro-cap.pdf'
LAN_N = 'https://cms-media.lannebo.se/sv/fonder/informationsbroschyr-lannebo-norden.pdf'
LAN_NOTE = ('Lannebo informationsbroschyr (Uppdaterad 23 okt 2025 and 1 dec 2025) states: "Lannebo tillampar justerat fondandelsvarde for foljande fonder: '
            'Lannebo High Yield (2%), Lannebo Rantefond Kort (1%), Lannebo Sustainable Corporate Bond (1%)". No equity fund is covered.')
OHMAN_NOTE = ('Ex-Ohman fund managed by Lannebo Kapitalforvaltning since the 2024 merger. Lannebo brochure (Oct/Dec 2025) lists only three fixed-income funds '
              'applying justerat fondandelsvarde; the Feb 2026 unitholder letter (effective 18/25 March 2026) lists every amended paragraph and introduces no such clause. '
              'Fondbestammelser of the Ohman-branded fund itself not read.')
LF_EV = 'https://www.lansforsakringar.se/stockholm/privat/bank/spara/fonder/fondhandelser/'
LF_NOTE_IDX = ('LF kundbrev 26 Nov 2024 "Andrade fondbestammelser for LF Global Index, Europa Index, Tillvaxtmarknad Index, USA Index, Japan Index" '
               '(https://www.lansforsakringar.se/4ad817/globalassets/aa-global/dokument/ovrigt/fondhandelser/2024/andrade-fondbestammelser-for-lansforsakringar.pdf) '
               'is a scanned PDF with no machine-readable text and could not be read. Later LF letters (16 Jun 2025 Sverige Index; 26 Jun 2026 four funds) contain no justerat fondandelsvarde clause.')
LF_NOTE_NOCHG = ('LF fondhandelser list (complete for 2025-2026, partial for 2024) shows no fondbestammelse change for this fund in 2024-2026 and no LF notice about justerat fondandelsvarde. '
                 'Fondbestammelser not read (LF site is JS-only). Treated as NO by absence of any rule change; downgrade to UNKNOWN if a 2023 change is found.')
HB_URL = 'https://www.handelsbanken.se/sv/privat/spara/fonder/fondandringar-handelsbanken-liv'
HB_NOTE = ('Handelsbanken kundbrev March 2024 (Sverige Tema/Norden Tema renamed, rules changed 2024-03-20; http://www.handelsbanken.se/tron/public/info/contents/v1/document/32-217266) '
           'lists all changes, none on justerat fondandelsvarde. Omnibus rule change for 70 funds effective 2025-10-10 (document 32-269298): readable part (p.1-32, incl. fixed-income funds) '
           'contains no justerat fondandelsvarde / justeringsfaktor / troskelvarde; the Norden (p.84) and Sverige (p.114) sections could not be read. No company-level adoption found.')

# --- EU_active 2024-03-25 ---
add(336826, 'Banque de Luxembourg Investments S.A. (BL SICAV)', 'Luxembourg', U, U, U, U, '', 'https://www.banquedeluxembourginvestments.com/bank/bli/homepage', U,
    'BLI website gives no prospectus link without JS; prospectus not read.')
add(916122, 'BlackRock (Luxembourg) S.A. (BlackRock Global Funds)', 'Luxembourg', U, U, U, U, '', '', U,
    'BGF prospectus not reachable in this run (blackrock.com fetch failed). Unverified expectation: BGF prospectus permits NAV adjustment (swing pricing) for net flows; must be checked in the BGF prospectus in force June 2024.')
add(696898, 'BlackRock (Luxembourg) S.A. (BlackRock Global Funds)', 'Luxembourg', U, U, U, U, '', '', U,
    'As for BlackRock Euro Markets.')
add(309492, 'Luxcellence Management Company S.A. / CB Fonder AB (advisor)', 'Luxembourg', U, U, U, U, '', 'https://cbfonder.se/dokument/', U,
    'cbfonder.se links prospectus to luxcellence.com/funds, which lists no fund documents; prospectus not read.')
add(901181, 'Danske Invest Management A/S (Danske Invest SICAV)', 'Luxembourg', U, U, U, U, '2026-08-13', 'https://www.danskeinvest.lu/docs/full_prospectus_di_sicav_en.pdf', U,
    'Danske Invest SICAV prospectus (Aug 2026) fund descriptions readable (no swing statement in the Europe profile) but the general "Investing in the Funds"/NAV sections, where a swing-pricing clause would sit, were beyond the text extraction limit. KID and factsheet (Sep/Oct 2026) do not mention swing pricing.')
add(764951, 'Evli Fund Management Company Ltd', 'Finland', 'NO', '', '', 'N/A', '2024-07-01', 'https://content.evli.com/fund/pdf/Fund_prospectus_Evli_mutual_funds.pdf', 'VERIFIED',
    'Evli fund prospectus dated 1 July 2024 (contemporaneous with exit 2024-06-24) read in full (129k chars): no swing pricing / dilution / adjusted NAV provisions for any fund. Evli Europe rules last approved 25.03.2022.')
add(814947, 'FIL Investment Management (Luxembourg) S.A. (Fidelity Funds)', 'Luxembourg', U, U, U, U, '', '', U,
    'Fidelity Funds prospectus not reachable (fidelity.se pages are JS-only). Unverified expectation: Fidelity Funds prospectus contains a swing pricing provision.')
add(566556, 'Fondbolaget Fondita Ab', 'Finland', 'NO', '', '', 'N/A', '2026-08-01', 'https://fondita.fi/wp-content/uploads/2026/08/fondita-rahastoesite-8-2026.pdf', 'VERIFIED',
    'Fondita prospectus 8/2026 and fund rules in force 15.4.2026 contain no swing pricing / adjusted NAV mechanism for any Fondita fund. Fund renamed Fondita Sustainable World 16.8.2024. Documents in force at exit (2024-07-08) not read, but no later introduction either.')
add(899773, 'Goldman Sachs Asset Management B.V. (Goldman Sachs Funds SICAV, ex NN (L))', 'Luxembourg', U, U, U, U, '', '', U,
    'GS Funds SICAV prospectus not reachable. Unverified expectation: prospectus permits swing pricing (ex-NN IP practice).')
add(899352, 'Goldman Sachs Asset Management B.V. (Goldman Sachs Funds SICAV, ex NN (L))', 'Luxembourg', U, U, U, U, '', '', U, 'As for GS Europe Equity.')
add(848770, 'Goldman Sachs Asset Management B.V. (Goldman Sachs Funds SICAV, ex NN (L))', 'Luxembourg', U, U, U, U, '', '', U, 'As for GS Europe Equity.')
add(492306, 'Lansforsakringar Fondforvaltning AB', 'Sweden', 'NO', '', '', U, '2025-12-09', LF_EV, 'SECONDARY', LF_NOTE_NOCHG + ' Only event for the fund: change of fund manager 2025-12-09 (after exit).')
add(564849, 'Nordea Funds Ltd (Finland)', 'Finland', 'NO', '', '', 'N/A', '', 'https://www.nordeafunds.com/fi/osittainen-joustava-hinnoittelumenetelma', 'SECONDARY',
    'Nordea Funds Ltd page on partial swing pricing lists 28 Finnish funds; first implementation dates 30 May 2024 / 13 June 2024 (max factor 1.75% for Finnish funds). Nordea European Stars is not on the list. Liquidity tools (incl. swing pricing) were added to the rules of all Finland-registered Nordea funds only from 16 April 2026 (nordea.se fund-change notice 13 Mar 2026). Exit 2024-06-24 therefore pre-dates any adoption. Caveat: the fund may since have been merged, which would also explain its absence from the list.')
add(810465, 'Pictet Asset Management (Europe) S.A.', 'Luxembourg', U, U, U, U, '', '', U,
    'Pictet prospectus not reachable. Unverified expectation: Pictet prospectus permits swing pricing.')
add(755090, 'S-Bank Fund Management Ltd', 'Finland', 'NO', '', '', 'N/A', '2026-03-27', 'https://dokumentit.s-pankki.fi/tiedostot/s-banken-europa-aktie-stadgar', 'VERIFIED',
    'Current fund rules (FIN-FSA 12.2.2026, in force 27.3.2026) and prospectus (1.9.2026) provide an anti-dilution levy (avgift for utspadningsskydd, max 2.00% of order value) but no swing pricing / adjusted NAV. Rules in force at exit (2024-06-26) not read; the levy is a 2026 addition, so NO at exit.')
add(122432, 'SEB Investment Management AB / SEB Funds AB', 'Sweden', 'NO', '2025-03-14', '1', 'N/A', '2025-02-10', SEB_URL, 'VERIFIED',
    'SEB introduced justerat fondandelsvarde (max 1%) in 41 funds incl. SEB Europafond from 14 March 2025, i.e. after the fund left PPM (2024-07-16). SEB applied for FI permission for its first fund (Nordenfond) on 5 June 2024, so no SEB fund had the tool before 2025.')
add(666495, 'Franklin Templeton International Services S.a r.l. (FTIF)', 'Luxembourg', U, U, U, U, '', '', U,
    'FTIF prospectus not reachable (franklintempleton.se JS-only). Unverified expectation: FTIF prospectus contains a swing pricing provision.')
add(865063, 'abrdn Investments Luxembourg S.A. (abrdn SICAV I)', 'Luxembourg', U, U, U, U, '', '', U,
    'abrdn SICAV I prospectus not reachable. Unverified expectation: prospectus provides a dilution adjustment (swing) mechanism.')
add(367698, 'abrdn Investments Luxembourg S.A. (abrdn SICAV I)', 'Luxembourg', U, U, U, U, '', '', U, 'As for abrdn Europe ex UK.')
add(238832, 'Alandsbanken Fondbolag Ab', 'Finland', 'NO', '2026-04-16', '5', 'N/A', '2026-04-16', 'https://assets.alandsbanken.com/pdf/fund/Alandsbanken-Placeringsfonder-Gemensamma-Stadgar_16.4.2026.pdf', 'VERIFIED',
    'Fund-specific rules (FIN-FSA 27.1.2022, in force 22.4.2022) contain no swing clause. Swing pricing ("flexibel prissattningsmetod", swing factor max 5%) entered the common rules of all Alandsbanken funds from 16.4.2026 (FIN-FSA 3.2.2026), i.e. after exit (2024-06-28). Alandsbanken UCITS annual report 2025 does not mention swing pricing.')

# --- EU_index 2024-10-31 ---
add(219170, 'DNB Asset Management AS', 'Norway', U, U, U, U, '', 'https://dnbam.com/vare-fond/fond/dnb-gront-skifte-norden', U,
    'DNB prospectus documents (documents.anevis-solutions.com) are blocked to automated readers. DNB AM shows "Svingprising: Ja" for DNB Global Indeks (A class) but the Europa Indeks page could not be read. Likely same company practice, not verified.')
add(479840, 'Lansforsakringar Fondforvaltning AB', 'Sweden', U, U, U, U, '2024-11-26', LF_EV, U, LF_NOTE_IDX)
add(570630, 'Lannebo Kapitalforvaltning AB (ex Ohman Fonder)', 'Sweden', 'NO', '', '', 'N/A', '2026-02-01', 'https://www.lansforsakringar.se/495244/globalassets/aa-global/dokument/ovrigt/fondhandelser/2026/information-till-andelsagare-ohman-marknad-europa.pdf', 'SECONDARY', OHMAN_NOTE)

# --- Global_index 2024-10-31 ---
add(680124, 'Avanza Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2024-09-17', 'https://investors.avanza.se/files/Avanza_fonder/Fondbestammelser/FB_Avanza_Global_2024-09-17.pdf', 'VERIFIED',
    'Fondbestammelser dated 2024-09-17 (version in force at exit 2025-04-10): paragraph 8 Vardering has no justerat fondandelsvarde / justeringsfaktor / troskelvarde clause. Avanza Fonder half-year report 2025 has no such disclosure.')
add(252411, 'Danske Invest Management A/S (Danske Invest SICAV)', 'Luxembourg', U, U, U, U, '2026-08-13', 'https://www.danskeinvest.lu/web/show_download.prospectus?p_vIsin=LU1349493178&p_vLanguage=en', U,
    'See Danske Invest SICAV Europe: general NAV/swing sections of the prospectus not readable; KID (16.9.2026) and factsheet (11.10.2026) silent on swing pricing.')
add(613729, 'Danske Invest Management A/S (Danske Invest SICAV)', 'Luxembourg', U, U, U, U, '2026-08-13', 'https://www.danskeinvest.lu/docs/full_prospectus_di_sicav_en.pdf', U, 'As for Danske Invest Global Index SI.')
add(362491, 'DNB Asset Management AS', 'Norway', 'YES', U, U, U, '2026-10-08', 'https://dnbam.com/vare-fond/fond/dnb-indice-global', 'SECONDARY',
    'DNB AM fund page for DNB Global Indeks (class A, NO0010582984; S class is the same fund) lists under Betingelser "Svingprising: Ja" (page data 2026-10-08). Prospectus/vedtekter blocked to automated readers, so the adoption date and max factor are unknown and the status at exit (2025-04-16) is inferred from a later company page.')
add(199753, 'Lannebo Kapitalforvaltning AB (ex Ohman Fonder)', 'Sweden', 'NO', '', '', 'N/A', '2026-02-01', 'https://www.lansforsakringar.se/494d56/globalassets/aa-global/dokument/ovrigt/fondhandelser/2026/information-till-andelsagarna-ohman-marknad-global.pdf', 'SECONDARY', OHMAN_NOTE)
add(658997, 'Lansforsakringar Fondforvaltning AB', 'Sweden', U, U, U, U, '2024-11-26', LF_EV, U, LF_NOTE_IDX + ' June 2026 letter for Global Index (share classes/fees) contains no swing clause.')
add(407064, 'Storebrand Fonder AB', 'Sweden', 'NO', '2025-09-01', '2', 'N/A', '2025-05-15', STB, 'VERIFIED',
    'Storebrand kundbrev May 2025: FI-approved amended fondbestammelser for 15 equity funds incl. Global All Countries introduce the option of justerat fondandelsvarde (max 2% per share class) from 1 September 2025, i.e. after exit (2025-04-29).')
add(393488, 'Storebrand Fonder AB', 'Sweden', 'NO', '2025-09-01', '2', 'N/A', '2025-05-15', STB, 'VERIFIED', 'As for Storebrand Global All Countries (Global Plus is in the same 15-fund list); exit 2025-04-29 precedes 2025-09-01.')

# --- Nordic_active 2025-02-19 ---
add(147512, 'DNB Asset Management AS', 'Norway', U, U, U, U, '', 'https://dnbam.com/vare-fond/fond/dnb-gront-skifte-norden', U,
    'DNB AM page for Gront Skifte Norden shows no Betingelser section; prospectus blocked. DNB applies svingprising in DNB Global Indeks; not verified for this fund.')
add(811117, 'Handelsbanken Fonder AB', 'Sweden', 'NO', '', '', U, '2024-03-20', HB_URL, 'SECONDARY', HB_NOTE + ' Exit 2025-06-26 precedes the Oct 2025 omnibus change, so the rules at exit are the March 2024 version.')
add(354290, 'Holberg Fondsforvaltning AS', 'Norway', 'YES', U, 'not stated', U, '2026-03-27', 'https://www.holberg.no/informasjon/svingprising-2', 'VERIFIED',
    'Holberg states it practises svingprising in Holberg Norge, Norden, Vekstmarkeder, Triton, Kreditt, Kreditt Fokus, Obligasjon Norden, Likviditet and OMF (company page, undated). Prospekt Holberg Norden dated 27.3.2026 section 5 and vedtekter paragraph 6 ("Fondet kan benytte svingprising") confirm; no numeric max factor or threshold is published. Documents post-date the exit (2025-06-24); adoption date not found (Norwegian VFF industry standard).')
add(598557, 'ODIN Forvaltning AS', 'Norway', 'YES', '2024-06-04', 'not stated', U, '2026-06-15', 'https://odinfond.no/funds/files/980146561/no/Prospekt%20med%20vedtekter.pdf', 'VERIFIED',
    'ODIN Norden prospectus (updated 15.06.2026) and vedtekter paragraph 6: "Det benyttes svingprising ved fastsettelse av andelsverdien i fondet ved netto tegning eller innlosing"; vedtekter approved by Finanstilsynet 04.06.2024, before exit 2025-06-24. Swing factor based on historical trading costs; no numeric maximum stated.')
add(484980, 'Simplicity AB', 'Sweden', 'NO', '', '', 'N/A', '2026-04-30', 'https://www.simplicity.se/wp-content/uploads/ARSBERATTELSER_2025_WEB.pdf', 'VERIFIED',
    'Simplicity annual report 2025 and half-year report 2026 contain no justerat fondandelsvarde / justeringsfaktor / swing / likviditetsverktyg text (FFFS 2013:9 31 kap. 48 b would require disclosure if applied). The Norden fund section itself was outside the readable excerpt; fondbestammelser not read.')
add(388298, 'Storebrand Asset Management AS (Delphi Fondene)', 'Norway', 'YES', U, U, U, '2026-04-01', 'https://www.storebrandam.com/globalassets/storebrand-asset-management/documents/reports/annual-reports-mutual-funds---english/annual-report-2025.pdf', 'VERIFIED',
    'Storebrand AM (Norway) annual report 2025 for Storebrand, Delphi and SKAGEN mutual funds, Note 1 accounting principles: "Storebrand employs swing pricing routines to prevent existing [unitholders bearing...]" (sentence truncated in extraction). Board report: Delphi Nordic received redemptions exceeding 10% of fund value in 2025 (the PPM redemption, June 2025) "without material impact on risk management or valuation". Fund-level clause and adoption date not read (Delphi prospectus not linked on delphi.no).')
add(820852, 'Swedbank Robur Fonder AB', 'Sweden', U, U, U, U, '', 'https://swedbankrobur.fondlista.se/sv/details/SE0000537722', U,
    'Fondbestammelser, informationsbroschyr and annual report are served from internetbank.swedbank.se (ConditionsEarchive), which could not be fetched. Swedbank Robur news 2026 (Nordenfond rule change effective 1 April 2026: share classes, objective, risk method) does not mention justerat fondandelsvarde. No company-level adoption found, but not excluded.')

# --- Nordic_smallcap 2025-02-19 ---
add(339473, 'Aktia Fund Management Company Ltd', 'Finland', U, U, U, U, '', 'https://www.aktia.fi/fi/tietoja-aktian-sijoituspalveluista', U,
    'Aktia fund pages not reachable; valuation principles (20.12.2025) and readable part of the 2025 annual report mention no swing pricing; Nordic Small Cap section not readable. Not conclusive.')
add(785493, 'Fondbolaget Fondita Ab', 'Finland', 'NO', '', '', 'N/A', '2026-04-15', 'https://fondita.fi/wp-content/uploads/2026/04/nordic-micro-cap-saannot-2026.pdf', 'VERIFIED',
    'Fondita Nordic Micro Cap rules (2026) and Fondita prospectus 8/2026: standard NAV, no swing pricing; redemption notice/pro-rata tools only. Exit 2025-06-04.')

# --- SE_active 2025-08-27 ---
add(344739, 'Aktie-Ansvar AB', 'Sweden', 'NO', '', '', 'N/A', '2026-05-28', 'https://www.aktieansvar.se/globalassets/aktie-ansvar/investera/dokument/arsberattelse-2025/arsberattelse-sverige-2025.pdf', 'VERIFIED',
    'Aktie-Ansvar informationsbroschyr 2026-05-28 (general sections) and Aktie-Ansvar Sverige arsberattelse 2025 contain no justerat fondandelsvarde / justeringsfaktor. Exit 2026-02-26.')
add(792697, 'C WorldWide Fund Management S.A. (C WorldWide SICAV)', 'Luxembourg', 'YES', U, 'not readable', U, '2025-11-20', 'https://cww.lu/media/vtzbbrdb/c-worldwide-20251120_prospectus_de.pdf', 'VERIFIED',
    'C WorldWide prospectus November 2025 (in force at exit 2026-01-23), Sub-Fund 9 C WorldWide Sweden pp. 55-56: units issued/redeemed at NAV "adjusted by any applicable Swing Factor, provided that the Threshold is exceeded". Same wording in all sub-funds and in the October 2026 prospectus. The chapter defining the Swing Factor maximum was beyond the readable part.')
add(973263, 'Danske Invest Management A/S (Danske Invest SICAV)', 'Luxembourg', U, U, U, U, '2026-08-13', 'https://www.danskeinvest.lu/web/show_download.prospectus?p_vIsin=LU1349495116&p_vLanguage=en', U, 'As for Danske Invest Europe SI: Sverige profile has no swing statement; general sections not readable.')
add(916189, 'Handelsbanken Fonder AB', 'Sweden', 'NO', '', '', U, '2025-10-10', HB_URL, 'SECONDARY', HB_NOTE + ' Exit 2026-04-07, so the rules at exit are the 10 Oct 2025 version; the Sverige section of that letter was not readable.')
add(106849, 'Indecap Fonder AB', 'Sweden', 'NO', '', '', U, '2025-08-25', 'https://www.lansforsakringar.se/4a5a7c/globalassets/aa-global/dokument/ovrigt/fondhandelser/2025/brev-till-andelsagare-i-indecap-guide-sverige-2025-08-25.pdf', 'SECONDARY',
    'Unitholder letter 25 Aug 2025 (FI approval 22 Aug 2025, effective 1 Sep 2025; fund renamed from Indecap Guide Sverige) lists all amended paragraphs (1, 4, 9, 11); no justerat fondandelsvarde clause. Full fondbestammelser not available on indecap.se. Exit 2026-02-03.')
add(904904, 'Lannebo Kapitalforvaltning AB (ex Ohman Fonder)', 'Sweden', 'NO', '', '', 'N/A', '2026-02-01', 'https://www.lansforsakringar.se/494d85/globalassets/aa-global/dokument/ovrigt/fondhandelser/2026/information-till-andelsagare-ohman-sverige.pdf', 'SECONDARY', OHMAN_NOTE + ' Renamed Lannebo Sweden All Cap 18 March 2026 (after exit 2026-03-16).')
add(146928, 'Lannebo Kapitalforvaltning AB', 'Sweden', 'NO', '', '', 'N/A', '2025-12-01', LAN_N, 'VERIFIED', LAN_NOTE + ' Fund merged 2025-11-20.')
add(490292, 'Lannebo Kapitalforvaltning AB', 'Sweden', 'NO', '', '', 'N/A', '2025-12-01', LAN_N, 'VERIFIED', LAN_NOTE + ' Sverige Plus unitholder letter 18 Sep 2025 (rules effective 22 Sep 2025) introduces no such clause.')
add(806869, 'Lannebo Kapitalforvaltning AB', 'Sweden', 'NO', '', '', 'N/A', '2025-12-01', LAN_N, 'VERIFIED', LAN_NOTE)
add(528133, 'Lansforsakringar Fondforvaltning AB', 'Sweden', 'NO', '', '', U, '', LF_EV, 'SECONDARY', LF_NOTE_NOCHG)
add(203067, 'Nordea Funds AB (Sweden branch of Nordea Funds Ltd)', 'Sweden', 'YES', U, '1.75', U, '2026-06-16', 'https://docs.fundconnect.com/GetDocument.aspx?clientid=i1g0xyvk-ztaq-jdr2-cm3y-0sshe4ukztmc&Isin=SE0000625238&lang=sv-SE&type=Prospectus&save=False', 'VERIFIED',
    'Nordea Swedish Stars informationsbroschyr dated 16 June 2026: "Fonden tillampar en justeringsfaktor om hogst 1,75 procent"; "Partiell justering av fondandelsvarde anvands i foljande fonder: Institutionella Aktiefonden Stabil/Sverige/Varlden, Institutionella Foretagsobligationsfonden, Nordea Alfa, Nordea Ideell Aktiefond, Nordea Smabolagsfond Sverige, Nordea Sverige Passiv, Nordea Swedish Stars"; FI permission referenced. Brochure post-dates exit (2026-03-25). Nordea Sweden announced on 3 May 2024 that it moves from full to partial adjustment of the unit value in "a number of our equity funds" from 30 May 2024, which implies the tool existed in Swedish Nordea equity funds before then, but the fund list was not published. Annual report 2025 Swedish Stars section (p. 572) not readable; applied factors therefore unknown.')
add(450981, 'ODIN Forvaltning AS', 'Norway', 'YES', '2024-06-04', 'not stated', U, '2026-06-15', 'https://odinfond.no/funds/files/980146634/no/Prospekt%20med%20vedtekter.pdf', 'VERIFIED',
    'ODIN Sverige prospectus (updated 15.06.2026) and vedtekter paragraph 6: svingprising used at net subscription/redemption; vedtekter approved by Finanstilsynet 04.06.2024, before exit 2026-03-12. No numeric maximum stated.')
add(643700, 'Pareto Asset Management AB', 'Sweden', 'NO', '', '', 'N/A', '2025-05-14', 'https://paretoam.com/uploads/Sverige/Fondbestammelser/Fondbestammelser-Pareto-Sverige.pdf', 'VERIFIED',
    'Fondbestammelser (header date 14 May 2025) paragraph 8: standard NAV, no justerat fondandelsvarde. Informationsbroschyr version 2026-05-27 and arsberattelse 2025: no such clause. Exit 2026-01-22.')
add(328021, 'Prior & Nilsson Fond och Kapitalforvaltning AB', 'Sweden', 'NO', '', '', 'N/A', '2025-03-01', 'https://priornilsson.se/static/1326f79da20b076da178b5c825f62534/Informationsbroschyr-april-2026.pdf', 'VERIFIED',
    'PriorNilsson informationsbroschyr (dated March 2025) has no justerat fondandelsvarde section; arsberattelse 2025 (Sverige Aktiv section) no disclosure. Exit 2026-02-17.')
add(158261, 'SEB Investment Management AB / SEB Funds AB', 'Sweden', 'YES', '2025-03-14', '1', U, '2025-02-10', SEB18, 'VERIFIED',
    'SEB kundunderrattelse 18: FI-approved fondbestammelser for SEB Sverige Expanderad (A, B utd, C HNW, D inst) allow justerat fondandelsvarde, max 1% per share class, from 14 March 2025; also item 32 in SEB\'s list of 41 funds (news 10 Feb 2025). Exit 2026-01-27. Whether the tool was actually activated for this fund before exit was not found (SEB activated it in Nordenfond from 3 April 2025); 2025 annual report not read.')
add(846527, 'SEB Investment Management AB (SEB Fund 1, Luxembourg)', 'Luxembourg', U, U, U, U, '', '', U,
    'SEB Fund 1 (Luxembourg) prospectus not reachable in this run. Exit 2025-11-10.')
add(339184, 'Spiltan Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2021-09-01', 'https://www.spiltanfonder.se/upl/files/260035/fondbestammelser.pdf', 'VERIFIED',
    'Current fondbestammelser (board 2021-03-12, FI 2021-06-18 dnr 21-8524, in force 2021-09-01): no justerat fondandelsvarde clause; helarsrapport 2025 no disclosure. Exit 2026-04-21.')
add(272898, 'Spiltan Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2008-06-25', 'https://www.spiltanfonder.se/upl/files/259740/fondbestammelser.pdf', 'VERIFIED',
    'Current fondbestammelser (FI 2008-05-26, in force 2008-06-25): no justerat fondandelsvarde clause (only a max 1% subscription/redemption fee accruing to the fund). Exit 2026-06-24.')

# --- SE_index 2025-08-27 ---
add(734491, 'Avanza Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2026-06-16', 'https://investors.avanza.se/files/Avanza_fonder/Informationsbroschyr/informationsbroschyr_avanza-zero_2026-06-16.pdf', 'VERIFIED',
    'Fondbestammelser 2023-05-04 and informationsbroschyr 2026-06-16: no justerat fondandelsvarde. No exit date recorded in the input.')
add(528894, 'Cicero Fonder AB', 'Sweden', U, U, U, U, '', 'https://cicerofonder.se/fonder/aktiespararna-direktavkastning/', U,
    'Cicero fund pages load documents dynamically; fondbestammelser/informationsbroschyr could not be retrieved. Exit 2026-02-27.')
add(610410, 'Evli Fund Management Company Ltd', 'Finland', 'NO', '', '', 'N/A', '2026-07-07', 'https://assets.evli.com/production/Evli.com/Documents/Mutual_funds/Fund_Rules/EN/Fund_rules_28.9.2026/s_eri_en.pdf', 'VERIFIED',
    'Evli prospectus 1 July 2024: no swing pricing for any fund. New rules (FIN-FSA 7.7.2026; common rules 11.2.2026; fund renamed Evli Atlas Sweden Enhanced Index from 28.9.2026) still contain no swing/dilution clause, only redemption restrictions. Exit 2025-12-29.')
add(577833, 'Lannebo Kapitalforvaltning AB (ex Ohman Fonder)', 'Sweden', 'NO', '', '', 'N/A', '2026-02-01', 'https://www.lansforsakringar.se/495087/globalassets/aa-global/dokument/ovrigt/fondhandelser/2026/information-till-andelsagare-ohman-marknad-sverige-bred.pdf', 'SECONDARY', OHMAN_NOTE)
add(587337, 'Lansforsakringar Fondforvaltning AB', 'Sweden', 'NO', '', '', U, '2025-06-16', 'https://www.lansforsakringar.se/49d715/globalassets/aa-global/dokument/ovrigt/fondhandelser/2025/kundbrev-lf-16-06-2025.pdf', 'SECONDARY',
    'LF kundbrev 16 June 2025 (FI-approved rule change for Sverige Index: benchmark change plus editorial clarifications incl. valuation) does not introduce justerat fondandelsvarde; the 26 June 2026 letter (share classes) neither. Full fondbestammelser not read. Exit 2025-11-20.')
add(292193, 'Skandia Fonder AB', 'Sweden', U, U, U, U, '', '', U, 'skandia.se is JS-only and skandiafonder.se blocks automated readers; no document retrieved. Exit 2025-12-29.')
add(212332, 'Storebrand Fonder AB', 'Sweden', 'YES', '2025-09-01', '2', U, '2025-05-15', STB, 'VERIFIED',
    'Storebrand kundbrev May 2025: amended fondbestammelser (FI-approved) for 15 equity funds incl. Storebrand Sverige introduce the option of justerat fondandelsvarde, max 2% per share class, from 1 September 2025; exit 2026-03-09. Whether a factor was actually applied (annual report 2025) not read.')
add(357658, 'Storebrand Fonder AB', 'Sweden', 'YES', '2025-09-01', '2', U, '2025-05-15', STB, 'VERIFIED', 'As for Storebrand Sverige (Sverige Plus is in the same list); exit 2025-11-20.')

# --- EU_smallcap 2026-05-28 (no exits yet) ---
add(538751, 'Allianz Global Investors GmbH (Allianz Global Investors Fund)', 'Luxembourg', U, U, U, U, '', '', U,
    'AGIF prospectus not reachable in this run. Unverified expectation: AGIF prospectus permits swing pricing.')
add(250167, 'Banque de Luxembourg Investments S.A. (BL SICAV)', 'Luxembourg', U, U, U, U, '', '', U, 'As for BL-Equities Europe.')
add(182759, 'Lannebo Kapitalforvaltning AB', 'Sweden', 'NO', '', '', 'N/A', '2025-12-01', LAN_N, 'VERIFIED', LAN_NOTE + ' Not yet exited.')

# --- SE_smallcap 2026-05-28 (no exits yet) ---
add(712299, 'Atle Fund Management AB (Humle Fonder)', 'Sweden', U, U, U, U, '2025-01-20', 'https://www.humlefonder.se/fond/humle-smabolagsfond', U,
    'Fondbestammelser (2025-01-20) and informationsbroschyr (2026-02-20) are hosted on humle.cdn.prismic.io, which blocks automated readers. Not yet exited.')
add(721035, 'C WorldWide Fund Management S.A. (C WorldWide SICAV)', 'Luxembourg', 'YES', U, 'not readable', U, '2025-11-20', 'https://cww.lu/media/vtzbbrdb/c-worldwide-20251120_prospectus_de.pdf', 'VERIFIED',
    'C WorldWide prospectus November 2025, Sub-Fund 8 (Sweden Small Cap) pp. 52-53: issue and redemption at NAV "adjusted by any applicable Swing Factor, provided that the Threshold is exceeded"; same in the October 2026 prospectus. Not yet exited.')
add(584912, 'Carnegie Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2026-09-30', 'https://www.carnegiefonder.se/wp-content/uploads/file-manager/pdfer/informationsbroschyr/svenska/Informationsbroschyr.pdf', 'VERIFIED',
    'Carnegie Fonder informationsbroschyr (updated 2026-09-30) section JUSTERAT FONDANDELSVARDE lists only Carnegie Investment Grade, Likviditetsfond, Obligationsfond and Strategifond (max 2%). Smabolagsfond not covered. Not yet exited.')
add(420463, 'Evli Fund Management Company Ltd', 'Finland', 'NO', '', '', 'N/A', '2024-07-01', 'https://content.evli.com/fund/pdf/Fund_prospectus_Evli_mutual_funds.pdf', 'VERIFIED',
    'Evli prospectus 1 July 2024: no swing pricing for any Evli fund; 2026 rules for the sister index fund still none. Current rules of Sverige Smabolag not read. Not yet exited.')
add(694539, 'Lannebo Kapitalforvaltning AB (ex Ohman Smabolagsfond)', 'Sweden', 'NO', '', '', 'N/A', '2026-02-01', 'https://www.lansforsakringar.se/494c2d/globalassets/aa-global/dokument/ovrigt/fondhandelser/2026/information-till-andelsagare-ohman-smabolagsfond.pdf', 'SECONDARY',
    'ISIN SE0000432775 = Ohman Smabolagsfond, renamed 18 March 2026. ' + OHMAN_NOTE + ' Not yet exited.')
add(416867, 'Lannebo Kapitalforvaltning AB (ex Ohman Sweden Micro Cap)', 'Sweden', 'NO', '', '', 'N/A', '2025-10-23', LAN_MC, 'VERIFIED',
    'Lannebo Sweden Micro Cap informationsbroschyr (Uppdaterad 23 okt 2025): fondbestammelser paragraph 8 has no justerat fondandelsvarde clause; brochure lists only High Yield, Rantefond Kort and Sustainable Corporate Bond as applying it. Not yet exited.')
add(515676, 'Lansforsakringar Fondforvaltning AB', 'Sweden', 'NO', '', '', U, '', LF_EV, 'SECONDARY', LF_NOTE_NOCHG + ' Not yet exited.')
add(103606, 'Skandia Fonder AB', 'Sweden', U, U, U, U, '', '', U, 'As for Skandia Sverige Exponering. Not yet exited.')
add(152181, 'Spiltan Fonder AB', 'Sweden', 'NO', '', '', 'N/A', '2020-07-03', 'https://www.spiltanfonder.se/upl/files/260104/fondbestammelser.pdf', 'VERIFIED',
    'Current fondbestammelser (FI 2020-07-03 dnr 20-10973): no justerat fondandelsvarde clause. Not yet exited.')

# ---------------------------------------------------------------------------
cols = ['round', 'award', 'fondnr', 'fondnamn', 'isin', 'kategori', 'avslutsdatum', 'mv_award_msek', 'forvaltare_panel', 'svensk_panel',
        'fund_company', 'domicile', 'swing_status_at_exit', 'swing_since', 'max_factor_pct', 'applied_disclosed',
        'evidence_doc_date', 'source_url', 'verification', 'notes']
rows_out = []
missing = []
for r in losers:
    f = F.get(r['fondnr'])
    if f is None:
        missing.append(r['fondnr']); continue
    p = last.get(r['fondnr'], {})
    rows_out.append(dict(round=r['round'], award=r['award'], fondnr=r['fondnr'], fondnamn=r['fondnamn'], isin=p.get('isin', ''),
                         kategori=r['kategori'], avslutsdatum=r['avslutsdatum'], mv_award_msek=round(float(r['mv_award']) / 1e6, 1),
                         forvaltare_panel=p.get('forvaltare', ''), svensk_panel=p.get('svensk', ''),
                         fund_company=f['fund_company'], domicile=f['domicile'], swing_status_at_exit=f['swing_status'],
                         swing_since=f['swing_since'], max_factor_pct=f['max_factor_pct'], applied_disclosed=f['applied_disclosed'],
                         evidence_doc_date=f['evidence_doc_date'], source_url=f['source_url'], verification=f['verification'], notes=f['notes']))
assert not missing, missing
with open(OUT + 'swing_status_ftn_losers.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows_out)

# summary by round
summ = collections.defaultdict(lambda: collections.Counter())
for r in rows_out:
    summ[(r['round'], r['award'])][r['swing_status_at_exit']] += 1
print('round,award,YES,NO,UNKNOWN,total')
tot = collections.Counter()
for (rd, aw), c in sorted(summ.items(), key=lambda kv: kv[0][1]):
    print(f"{rd},{aw},{c['YES']},{c['NO']},{c['UNKNOWN']},{sum(c.values())}")
    tot.update(c)
print('TOTAL', dict(tot))
vc = collections.Counter(r['verification'] for r in rows_out)
print('verification', dict(vc))
dc = collections.Counter((r['domicile'], r['swing_status_at_exit']) for r in rows_out)
print('domicile x status', sorted(dc.items()))
json.dump({'by_round': {f"{k[0]} ({k[1]})": dict(v) for k, v in summ.items()}, 'total': dict(tot), 'verification': dict(vc)},
          open(OUT + 'summary.json', 'w'), indent=1)

# ---------------------------------------------------------------------------
# 2019 purge list
cand = json.load(open(OUT + 'purge2019_candidates.json'))
top = cand[:60]
def dom(isin, svensk):
    p = (isin or '')[:2]
    return {'SE': 'Sweden', 'FI': 'Finland', 'LU': 'Luxembourg', 'IE': 'Ireland', 'GB': 'United Kingdom', 'NO': 'Norway', 'DK': 'Denmark',
            'XS': 'Luxembourg (XS ISIN; C WorldWide SICAV)'}.get(p, 'Sweden' if svensk == 'Svensk' else 'Unknown')
notes2019 = {
    'Nordea Funds Ab': 'Nordea Funds Ltd (Finland) first applied partial swing pricing from 30 May 2024; no swing pricing in 2019 (company page).',
    'Ålandsbanken Fondbolag Ab': 'Alandsbanken fund-specific rules of 2022 had no swing clause; swing pricing entered the common rules only 16.4.2026. No swing pricing in 2019.',
    'C WorldWide Fund Management S.A.': 'Current C WorldWide SICAV prospectus (Nov 2025/Oct 2026) applies a Swing Factor in all sub-funds; the 2019 prospectus was not checked.',
    'C WorldWide Fund Management S,A,': 'Current C WorldWide SICAV prospectus (Nov 2025/Oct 2026) applies a Swing Factor in all sub-funds; the 2019 prospectus was not checked.',
    'Amundi Luxembourg S.A.': 'Not checked. Unverified expectation: Amundi Funds prospectus contained a swing pricing provision in 2019.',
    'J.P. Morgan Asset Management (Europe) S.à r.l.': 'Not checked. Unverified expectation: JPMorgan Funds prospectus contained a swing pricing provision in 2019.',
    'Morgan Stanley Investment Management Ltd': 'Not checked. Unverified expectation: MSINVF prospectus contained a swing pricing provision in 2019.',
    'UBS Fund Management (Luxembourg) S,A': 'Not checked. Unverified expectation: UBS (Lux) Equity SICAV prospectus contained a swing pricing provision in 2019.',
    'First State Investments (UK) Ltd': 'UK OEIC: dilution adjustment/levy regime (COLL); not checked.',
}
cols2 = ['rank_by_max_mv', 'fondnr', 'fondnamn', 'isin', 'forvaltare_panel', 'svensk_panel', 'domicile', 'kategori', 'first_month_in_panel', 'last_month_in_panel',
         'mv_max_2018_19_msek', 'mv_last_msek', 'swing_possible_2019', 'swing_2019_status', 'verification', 'notes']
rows2 = []
for i, d in enumerate(top):
    domicile = dom(d['isin'], d['svensk'])
    if domicile == 'Sweden':
        poss = 'NO'; st = 'NO'; ver = 'VERIFIED (legal)'
        note = 'Swedish UCITS: justerat fondandelsvarde not available in law before 1 July 2023 (LVF 4 kap. 10 b, SFS 2023:234).'
    else:
        poss = 'YES (foreign UCITS; depends on prospectus)'
        n = notes2019.get(d['forvaltare'], '')
        if d['forvaltare'] in ('Nordea Funds Ab', 'Ålandsbanken Fondbolag Ab'):
            st = 'NO'; ver = 'SECONDARY'
        else:
            st = 'UNKNOWN'; ver = 'UNKNOWN'
        note = n or 'Prospectus around 2019 not checked (no search budget / documents not reachable in this run).'
    rows2.append(dict(rank_by_max_mv=i + 1, fondnr=d['fondnr'], fondnamn=d['fondnamn'], isin=d['isin'], forvaltare_panel=d['forvaltare'], svensk_panel=d['svensk'],
                      domicile=domicile, kategori=d['kategori'], first_month_in_panel=d['first_month'], last_month_in_panel=d['last_month'],
                      mv_max_2018_19_msek=round(d['mv_max_2018_19'] / 1e6, 1), mv_last_msek=round(d['mv_last'] / 1e6, 1),
                      swing_possible_2019=poss, swing_2019_status=st, verification=ver, notes=note))
with open(OUT + 'swing_status_2019_purge.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols2); w.writeheader(); w.writerows(rows2)
print('2019 list domiciles', collections.Counter(r['domicile'] for r in rows2))
print('2019 status', collections.Counter(r['swing_2019_status'] for r in rows2))
