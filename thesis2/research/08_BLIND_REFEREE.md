# 08. Blind referee: Plan A (SSZ, financethesis_ny/PLAN.md) versus Plan B (file 07)

Run 11 Oct 2026, 22:05, by an agent with no context from the day's work. It read referee_C.md (the 5 Oct rejection of price pressure), PLAN.md, the 5 Oct decision record and judge memo, and files 01, 02, 06 and 07 here. Verbatim below; the editor's response follows.

## 1. Referee C's objections against Plan B

| ID | Plan B | Reason |
|---|---|---|
| F1 anchor/test | PARTLY | GS fits announce/execute/revert (07), but execution days are unpublished (06 fact 7): "pre-announced" fails at execution; replication mean-CAR, extension cross-sectional slope |
| S1 replication | PARTLY | Data-level OMXS30 leg exists; "40 to 60 events, by rough count" (07) is a guess |
| S2 one-stock tail | PARTLY | Sell-side-only spec (07 Table 3) sidesteps Edge; small-cap sd 0.56 to 0.73 is the old net-FIP number (06 fact 8) |
| S3 power | PARTLY | CAR sd assumed, not estimated; Nordic (sd 0.04 pp) adds nothing; quarterly Lou benchmark against a 7-day window |
| S4 common shock | OPEN | Within-round permutation RI (07) cannot absorb an event-week style shock |
| S5 award news | PARTLY | Argued from saver inertia (06 facts 1, 6); non-PPM flows unmeasured |
| S6 grader's bar | NOT ADDRESSED | Sabbatucci's paper, leave-one-out, bounded claims: absent |
| S7 synopsis | PARTLY | Fees, default, supply in Table 1 (06 facts 3 to 6); no Klug sign-off |
| S8 data, calendar | OPEN | List grew (07 Data): all-market LSEG, five FI quarters, execution days (I-15, planned), swing rules; FI 2026Q3 assumed by week 5 (I-19) |
| M1 post-event caps | PARTLY | "Uses no prices" asserted (07); 06 fact 8 divides SEK by cap, dates unstated |
| M2 matching | NOT ADDRESSED | Inherits agentP vectors (06 fact 8) |
| M3 controls | PARTLY | No B/M, no industry FE |
| M4 precision claim | CLOSED | Not made |
| M5 Europe small-cap | NOT ADDRESSED | |
| M6 placebo | NOT ADDRESSED | Index round is low-dose treated, signs predictable (06 fact 8) |
| M7 pre-trading | PARTLY | FI quarters before/after (07); not on disk |
| M8 go/no-go | CLOSED | MDE against a stated range (07 Power) |

## 2. New objections

- Calendar. Exec+40 trading days for a small-cap execution after 8 Oct lands after 7 Dec; 06 says only "Oct 2026, in progress".
- Where the fund trades. The agency redeems on one day; a manager warned two weeks earlier sells over [letter, exec]. The MDE uses a 7-day CAR sd; over two to three months small-cap CAR sd is 15 to 20 per cent and the MDE triples.
- Netting is back. Swedish active legs correlate 0.82 to 0.89; winners bought 45/36 per cent in the months losers sold 51/34 (06 facts 7, 8). Sell-only pressure overstates the net shock threefold.
- The replication cannot show the anchor's result: OMXS30 trackers hold little of index market cap, so the effect may always have been near zero; 20 to 30 events per sub-period gives an MDE of 4 to 5 per cent.
- Grader and fan-out. Sabbatucci's own working-paper question, with approximate caps and two usable rounds; two anchors, five tables, three figures, a cost-benefit: the fan-out the winners audit flagged.

## 3. Motivated reasoning

- "One pre-announced day" (07 opening) against "exact days are not published" (06 fact 7).
- "The letter alone moves nothing": fact 1 does not show a letter was sent in the frozen round, and it measures saver inertia, not market information.
- "Two independent routes": fact 8 reuses the revised folder's agentP vectors.
- "Reversal window in early December": true only for execution by 8 Oct.
- Every outcome wins: a null OMXS30 effect "sharpens the question"; an index-round null is the placebo, a non-null an ESG paragraph.
- Plan A dismissed as "household finance" in one line; DC plans are the grader's field.

## 4. The case for A that B ignores

A's headline needs no 2026 data, no LSEG, no execution dates: N 512, MDE 0.10, over 99 per cent power against SSZ's +0.185 and the predicted no-sponsor gap. B never mentions calendar risk; its week-3 unblinding runs on data not on disk. A's weaknesses survive the deadline; B's may not.

## 5. Verdict

Start Monday on A. Pass by 7 Dec: A 0.85, B 0.60. Prize: A 0.08, B 0.18. B is the better thesis if built and the worse bet in eight weeks: its risks are data and calendar, which no specification removes, and nobody has refereed it. Flip condition, Friday 17 Oct: the LSEG daily panel (Nasdaq Stockholm and First North, 2005-2026) and a counted OMXS30 change list are on disk, and the small-cap execution day is visible in daily TNA, dated no later than 8 Oct. Both met: switch to B. Otherwise A stands.

## Editor's response (main session, after reading)

Accepted as written. The six motivated-reasoning items are fair and file 07 should be read with them: the execution day is dated from daily TNA, not published; the appeal-round fact shows saver inertia, not that the market was uninformed; the pressure vectors come from the same FI parsing as the revised folder; the 40-day reversal window closes before 7 Dec only if the small-cap execution happened by about 8 Oct; and the two-sided "every outcome wins" framing must go, with one pre-registered prediction per table. The netting objection is the most important new one: the sell-side-only specification needs a net column reported with equal weight, and the MDE must be recomputed over the [letter, exec] window, not seven days.

The verdict's structure is adopted: one week of gated work, decision Friday 17 Oct with Klug. See the plan in the chat of 11 Oct and the calendar below.

Week of 13 to 17 Oct, both tracks in parallel:
- Track A (data on disk): run the SSZ replication table on the PPM panel (PLAN.md section 4), so Plan A's headline exists by Friday whatever happens. This is also the fallback.
- Track B gate: pull the LSEG daily panel (Nasdaq Stockholm and First North, 2005-2026, price, volume, shares, cap); count OMXS30 changes 2005-2026 from Nasdaq press releases; read the Swedish small-cap execution day off daily TNA in the SHoF files. Three yes/no checks.
- Friday 17 Oct: meeting with Klug. Both plans on the table, this file, and the three checks. Gate met: Plan B, with the corrections above. Gate not met: Plan A with Table 1 from file 06 bolted on. Synopsis drift needs Klug's written sign-off in either case.
