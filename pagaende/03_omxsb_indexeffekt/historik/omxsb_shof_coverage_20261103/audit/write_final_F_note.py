from pathlib import Path
import pandas as pd,json
O=Path(__file__).resolve().parent;W=O.parents[1]
stages=[('A/B/C',O/'overall_allcell_summary.csv',O/'event_all8cell_coverage.csv'),('D',O/'D_overall_coverage_summary.csv',O/'D_event_all8cell_coverage.csv'),('E',O/'E_overall_coverage_summary.csv',O/'E_event_all8cell_coverage.csv'),('F',O/'F_overall_coverage_summary.csv',O/'F_event_all8cell_coverage.csv')]
rows=[]
keep=['A','B','C','D_RIPS_hybrid','D_RIPS_pilot','D_NAV_conditional_hybrid','D_NAV_conditional_pilot','E_RIPS_hybrid','E_RIPS_newraw15','E_NAV_conditional_hybrid','E_NAV_conditional_newraw15','F_RIPS_allraw','F_NAV_conditional_allraw']
for stage,sp,ep in stages:
 S=pd.read_csv(sp);EV=pd.read_csv(ep)
 for x in S[S.scenario.isin(keep)].itertuples():
  d=EV[EV.scenario.eq(x.scenario)];rows.append(dict(stage=stage,scenario=x.scenario,events=x.events,mean_capital_coverage_pct=100*x.equal_cell_mean_fraction,pooled_fixed_price_capital_coverage_pct=100*x.pooled_SEK_coverage_fraction,events_all8_ge50=int(d.all8_ge_50.sum()),events_all8_ge75=int(d.all8_ge_75.sum()),events_all8_ge90=int(d.all8_ge_90.sum()),old_monthly_provisional_included=x.scenario in ['A','B','D_RIPS_hybrid','D_NAV_conditional_hybrid','E_RIPS_hybrid','E_NAV_conditional_hybrid'],conditional_NAV='NAV_conditional' in x.scenario))
pd.DataFrame(rows).to_csv(O/'FINAL_A_TO_F_COVERAGE_COMPARISON.csv',index=False)
P=W/'shof_coverage_20261103/source_method/existing_A_raw/EXISTING_A_RAW_FUND_REVIEW_SOURCE_ELIGIBILITY.csv'
S=pd.read_csv(P,dtype={'FI_fund_id':str});bad=S[S.in_frozen_old_A_pair&~S.D_RIPS_ECB_source_supported];bad.to_csv(O/'F_oldA_rejected_raw_source_pairs.csv',index=False)
dec={'scope':'Source-to-fixed-population feasibility only; no economic outcomes.','raw_source_data_review_complete_for_requested178funds':True,'old_monthly_flags_used_in_finalF':False,'GO_for':'Precisely defining the raw-source-covered fund subset and designing a separate locked accounting/precision/pass-through validation.','NOT_GO_for':['A claim about fundingrisk of the full FI-owner population or the whole stock market.','Treating the conditionalNAV series as certifiedtotalreturn without resolving its assumptions.','A causal priceeffect or riskfinding.','Opening multiple economic outcomes and choosing windows/samples by significance.'],'why':'Substantialowner capital remains outside sourcecoverage. Unrestricted missing-owner flowvariances and crosscovariances can strengthen or cancel observedsubset demandvariance. Coverage thresholds alone are not power or identification.','before_any_economic_risk_measure':['Lock the target as a definedcoveredfundpopulation, preserving sameevent/control/fundsupport.','Validate accounting units, distributions/classmigration/FXfixing and estimatedflow precision with independent sourcecomparisons where available.','Keep nativeRIPS and conditionalNAV apart; currentmaster classuniverse/ECBfixing assumptions stay explicit.','Validate or explicitly assume flow-to-stock trading pass-through; quarterly holdings do not identify eventorders.'],'previous_A_rawrejections':{'fundreview_pairs':len(bad),'distinct_funds':bad.FI_fund_id.nunique()},'thresholds_not_used_as_GO_rule':True,'no_returns_flows_covariance_or_risk_estimated':True}
(O/'FINAL_SOURCE_DECISION_SCOPE.json').write_text(json.dumps(dec,indent=2))
note='''F: slutlig rådatabaserad kapitaltäckning — 3 november 2026
Tekniskt beslutsunderlag, inte uppsatstext. Den begärda källkontrollen är genomförd för 178 fonder. F använder inga gamla månadsflaggor som reserv. Inga fondavkastningar, nettoflödesmått, kovarianser, prisresponser eller riskutfall har beräknats.

Slutlig täckning, exakt samma 135 händelser och ursprungliga kontrollaktier:
                                      Medel celler   Kapitalvägt
F, endast levererad RIPS                    51,71%       51,34%
F, inklusive separat villkorad NAV           55,91%       54,35%

RIPS-varianten når minst 50% av kapitalet i alla åtta aktie/ändpunktsceller för 13 av 135 händelser. NAV-inkluderande varianten når det för 30. Ingen variant når 75% eller 90% i samtliga celler för någon händelse. Detta är täckningsbeskrivning, ingen styrkeberäkning eller automatisk beslutströskel.

De fasta fondpopulationerna och nämnarna är oförändrade. Samma kvalificerade fond-ID används för eventaktien, alla tre kontrollaktier och båda ändpunkterna. RIPS ger 1 160 kvalificerade fond/omviktningspar i den fasta populationen; den villkorade NAV-varianten ger 1 175. Den ursprungliga rapportpopulationen, inte positiva innehav, avgör vilka fonder som kan ingå.

Varför den sista rådatakontrollen var nödvändig:
56 tidigare A-pass i 14 fonder underkänns av den nya rådatagrinden. De har tagits bort, inte dolts av äldre månadsmetadata. Nya historiker fyller samtidigt andra luckor, särskilt tidigare år. Därför ökar den genomsnittliga täckningen jämfört med E, men antalet händelser som når 50% i alla celler minskar från 16 till 13 i RIPS-varianten. Det är inget motsägelsefullt: genomsnitt och den svagaste cellen mäter olika saker.

Jämförelsen är nu spårbar:
A:32,45% medel, äldre preliminära källflaggor.
B:37,69%, fem råpiloter uppdaterade med strikt tidigare grind.
D RIPS:39,66%, daterade klasser/valuta för dessa fem.
E RIPS:49,70%, ytterligare tio råfonder men fortfarande äldre flaggor för övriga.
F RIPS:51,71%, enbart rådatagrindar för samtliga 178 begärda fonder.
A/B/C/D/E ligger kvar oförändrade. Den fullständiga jämförelsen med villkorad NAV och pilot-only-varianter finns i FINAL_A_TO_F_COVERAGE_COMPARISON.csv.

Beslutets räckvidd:
Ja till att definiera den rådatatäckta fondgruppen och förbereda en separat, fast validering av redovisning och uppskattade flöden. Nej till att redan nu hävda en ekonomisk riskförändring för hela FI-ägarbasen eller marknaden. Den återstående kapitalandelen saknar kvalificerad källa, och okända flödesvarianser och korskovarianser kan förstärka eller motverka den täckta gruppens efterfrågevariation. En hög täckningsprocent ensam löser inte detta.

RIPS är leverantörens totalavkastningsdata; NAV-varianten är fortfarande uttryckligen villkorad. ECB-kurser är referenskurser och är inte nödvändigtvis fondens NAV-valutafixing. Klassmigration, utdelningar, hela den historiska klassförteckningen och sambandet mellan fondflöden och aktiehandel behöver fortsatt ekonomisk metodkontroll innan riskmått tolkas. Källgranskningen certifierar inte observerade kontantflöden eller eventorder.

Verifiering: F byggs från råa FI-innehav och råkällornas kvalificeringsflaggor. Alla 937 gamla A-bidrag ersätts; ingen A-fallback eller dubbelräkning används. Oberoende rekonstruktion av frysta A/C/D avviker högst 2,24e-16 av kapitalnämnaren. Täckningsandelar ligger inom [0,1]; saknad nämnare skulle bevaras som NA. Inga nämnare saknas här. Tidigare resultatfiler och källval har inte ändrats.
'''
(O/'REPORT_F_FINAL_SV.txt').write_text(note)
print(pd.DataFrame(rows).to_string(index=False));print('Finalsource decision and report complete.')
