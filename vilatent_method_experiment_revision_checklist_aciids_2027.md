# ViLatent – Method & Experiment Revision Checklist (ACIIDS 2027)

Oct 25, 2026 · @Kie

## Summary

Submit to ACIIDS 2027 before Oct 31, 2026 (AoE, via EasyChair). The paper's focus shifts to: when is soft memory more worthwhile than text under the same token budget. Primary setting is ViQuAD-Long at $4\times$.

**Finalized Decisions**

- Dev/debug on $2\times\text{T4}$ Kaggle; all metrics reported in the paper are strictly taken from 1–2 H100s.
- ViQuAD-Long uses the full article, with no length limit.
- Soft baseline: frozen writer $L=4$, training only the adapter (referred to as LatentPress-style, not a strict reproduction).
- Multi-rate writer: a single stage-1 run used across all compression ratios.
- Fallback changed to a 3-stage cascade with an answer-in-evidence check.

**Pending Confirmation** (the doc currently assumes the recommended options)

- [ ] Is the actual deadline Oct 31? The official website still states Sep 30.
- [ ] Full article source: (a) all passages in ViQuAD — recommended; or (b) actual Wikipedia articles.
- [ ] Primary setting = ViQuAD-Long $4\times$ (finalize before B12).
- [ ] LNCS/LNAI page limit for ACIIDS.
- [ ] Are there any reusable stage-1/stage-2 checkpoints available?

## A. Paper Text Revisions

Complete A1–A14 and A22–A24 on Oct 26–27, before getting the numerical results. A13 must be finalized before B12 so the decision rule remains pre-specified. Fill in the numbers for A15–A20 and A25 on Oct 29–30. Priority levels: \[Mandatory\] / \[Nice-to-have\] / \[If time permits\].

### Abstract + §1 Introduction

- [ ] **A1** \[Mandatory\] Change the claim: from "ViLatent beats hard compression at $4\times$" to "when is soft memory more worthwhile than text under the same budget". ME remains the primary system.
- [ ] **A2** \[Mandatory\] Rewrite the 3 RQs:
  - RQ1: ME vs. hard compression on ViQuAD-Long and single-passage, at $4\times / 8\times / 16\times$; the advantage comes from memory content, not style learning.
  - RQ2: keep as is (the cost of query-blind writing).
  - RQ3: how many tokens a cascade fallback needs to retain 95% F1 of full-context.
- [ ] **A3** \[Mandatory\] Contributions: add multi-rate writer (1 checkpoint for all ratios), ViQuAD-Long (long document), end-to-end cost accounting for the writer. Hedge the "first" claim with "to our knowledge".

### §3 ViLatent (Method)

- [ ] **A4** \[Mandatory\] §3.2 Multi-rate writer: $h_t$ does not depend on $\rho$, so train 1 writer with $\rho$ randomly sampled from $\{4, 8, 16, 32\}$. $W_a$ and $s$ are shared across all $\rho$. Remove the sentence "each with its own stage-1 run".
- [ ] **A5** \[Mandatory\] §3.3 BM25: change "lowercased syllables" to word-segmented tokens (pyvi or VnCoreNLP), removing question words (ai, gì, nào, bao nhiêu…). The BM25 baseline uses the same preprocessing.
- [ ] **A6** \[Mandatory\] §3.3 Turn MEF into a 3-stage cascade: (1) ME answers; (2) if the answer is not verbatim in the evidence (answer-in-evidence, AiE) or $\text{log-prob} < \tau$, switch to BM25 with a budget of $2k(r)$; (3) if it still fails, read the full context. Select $\tau$ on the select split; clearly state the token cost at each stage.
- [ ] **A7** \[Mandatory\] §3.4 Training: stage-2 randomly samples $r \in \{4, 8, 16\}$ and $f \in \{1, 2, 4, 8\}$; $f=1$ is specifically ViLatent-M. Add a sentence: teacher logits are computed once and cached.
- [ ] **A22** \[Mandatory\] §3.4 Training: stage-2 mixes in about 30% multi-passage samples (concatenating 2–8 passages from the same article, from the train set) so the reader gets used to reading long memory sequences.
- [ ] **A8** \[Mandatory\] Table 1: update the MEF row to cascade; note that M is a special case of ME with $f=1$.
- [ ] **A9** \[Nice-to-have\] §3.3 ViLatent-Q: clearly state it only runs at $r=4$, serving a diagnostic role (if B13-Q is cut, shift RQ2 to comparing M with ME).

### §4 Experimental Setup

- [ ] **A10** \[Mandatory\] §4.1 ViQuAD-Long: concatenate all passages from the same article in their original JSON order, with no length limit; answerable questions only; splits inherited by article; applied to gate, select, and test; used for evaluation only. Report min / median / max tokens and deduplication method.
- [ ] **A11** \[Mandatory\] §4.2: update writer configuration to multi-rate; update the number of seeds to match what was actually run.
- [ ] **A12** \[Mandatory\] §4.3 add baselines: PhoBERT sentence selector (hard, trained, label "sentence contains the answer"); word-segmented BM25.
- [ ] **A23** \[Mandatory\] §4.3 frozen writer baseline $L=4$, training only the adapter, $s$, and boundary embeddings. Add a sentence: we do not use $L=2$ like LatentPress because the first 2 layers of Qwen3.5 are DeltaNet, lacking attention.
- [ ] **A13** \[Mandatory\] §4.4 Decision rule: primary = ViQuAD-Long at $4\times$, keeping the 3 original conditions; single-passage and $8\times / 16\times$ are descriptive analyses. Add a sentence explaining the $+3$ F1 threshold. Finalize before B12.
- [ ] **A24** \[Mandatory\] §4.4 Statistics: article-level bootstrap is primary, passage-level is secondary (Long only has 19 test articles).
- [ ] **A14** \[Mandatory\] Cost metrics: end-to-end latency including writer + BM25 + reader; break-even point in terms of number of questions per document.

### §5 Results (set up the skeleton first, fill in numbers later)

- [ ] **A15** \[Mandatory\] Table 2 (primary, Long $4\times$): add rows for PhoBERT selector, word-segmented BM25, and frozen writer.
- [ ] **A16** \[Mandatory\] New figure: F1 across compression ratios $4 / 8 / 16\times$ for BM25, PhoBERT, M, ME, and learned prompt — the central figure for the crossover narrative.
- [ ] **A17** \[Mandatory\] Table 3 (by $f$): note "single checkpoint, varying only $f$ at inference".
- [ ] **A18** \[Nice-to-have\] Secondary setting table: single-passage at $4\times$.
- [ ] **A19** \[Nice-to-have\] Figure 2 (fallback): 2 curves for log-prob and AiE + cascade; accompanied by an ECE metric (Expected Calibration Error — discrepancy between confidence and accuracy).
- [ ] **A20** \[Nice-to-have\] Cost table: latency and break-even point.
- [ ] **A25** \[Nice-to-have\] F1 by the position of the answer-containing passage within the article (beginning / middle / end).

### §6 Limitations

- [ ] **A21** \[Mandatory\] Add: multi-rate training might underperform dedicated per-rate training; small number of seeds; ViQuAD-Long consists of concatenated passages from the dataset rather than full Wikipedia articles; only 19 test articles. Future Work: query-dependent readout like Memorilla, attention-pooling, 9B reader, comparison with English.

## B. Code and Experiments

In total: 1 stage-1 run and 4–5 stage-2 runs, covering 3 compression ratios $\times$ 4 values of $f$ $\times$ 2 settings (Long, single-passage). Measure time per step in the first run to finalize the schedule for the following days.

| ID | Task | Machine | Date | Priority |
| --- | --- | --- | --- | --- |
| B1 | Test Qwen3.5's Gated DeltaNet kernel on T4 (1 batch, fp16) | T4 | Oct 26 | Mandatory |
| B2 | Code multi-rate (sampling $\rho, r, f$) + multi-passage mixing; test on 50 samples | T4 | Oct 26 | Mandatory |
| B3 | Word-segmented BM25 + question word removal; measure rate of truncated answers | CPU | Oct 26 | Mandatory |
| B4 | Build ViQuAD-Long full article; length statistics; verify all answers remain in context | CPU | Oct 26 | Mandatory |
| B5 | Train PhoBERT sentence selector | T4 | Oct 26–27 | Mandatory |
| B6 | Cache teacher logits, including multi-passage samples | H100 #1 | Oct 26 | Mandatory |
| B7 | Hard baselines $\times \{4, 8, 16\}\times \times \{\text{gate}, \text{select}\} \times \{\text{Long}, \text{single-passage}\}$; run full context on Long early as it is heavy | H100 #2 | Oct 26–27 | Mandatory |
| B16 | Measure distribution of answer positions in the article; script for F1 by position | CPU | Oct 27 | Nice-to-have |
| B11 | Code cascade + AiE + ECE; script to measure end-to-end latency | T4/CPU | Oct 27 | Mandatory |
| B8 | Stage-1 multi-rate | H100 #1 | Oct 27 | Mandatory |
| B9 | Stage-2 ME/M multi-rate, mixing 30% multi-passage, seed 1 (if short on time, reduce to 15%, do not drop) | H100 #1 | Oct 28 | Mandatory |
| B10 | Stage-2 learned prompt + BM25, multi-rate | H100 #2 | Oct 28 | Mandatory |
| B12 | Evaluate on gate $\rightarrow$ check decision rule $\rightarrow$ select $f^*$ and $\tau$ on select | H100 #1 | Oct 29 | Mandatory |
| B13 | Frozen writer $L=4$, stage-2 multi-rate only, identity-initialized adapter | H100 #2 | Oct 29 | Mandatory |
| B14 | Run test exactly once: all tables + swapped memory + cascade + latency, both Long and single-passage | H100 #1 | Oct 30 | Mandatory |
| B17 | ViLatent-Q at $r=4$ (RQ2) | H100 #2 | Oct 30 | If time permits |
| B15 | Seed 2 for ME and learned prompt | H100 #2 | Oct 30 | If time permits |

Cut completely, move to Limitations: separate training per $f$, seed 3, attention-pooling, query-dependent readout, 9B reader.

## 6-Day Schedule

&#91;embedded content: machine schedule · Oct 26–31, 2026\]

H100 #1 runs the main pipeline: cache $\rightarrow$ stage-1 $\rightarrow$ stage-2 $\rightarrow$ gate $\rightarrow$ test. H100 #2 runs baselines and controls in parallel. If only 1 H100 is available: run B10 right after B9, drop B15 and B17.

## Principles, Risks, and Contingencies

**Principles**

1. Run each configuration once; select hyperparameters on the select split; run the test split exactly once on Oct 30.
2. Any outcome is publishable: the crossover curve across compression ratios is a solid contribution even if ME does not win at $4\times$.
3. Metrics in the paper are strictly taken from H100 (bf16); T4 is for debugging only.

**Risks and Mitigation**

| Risk | Indicator | Mitigation |
| --- | --- | --- |
| DeltaNet kernel fails to run on T4 | B1 errors out or is extremely slow | Debug directly on H100 with 50 samples, first thing on Oct 26 |
| fp16 overflow at early sequence positions on T4 | NaN loss during debugging | Only verify code logic on T4, ignore numerical values |
| Reader fails to process long memory sequences | ME on Long significantly underperforms ME on single-passage | Keep the multi-passage mixing ratio in B9; report it as a finding in §5 |
| B6/B9 is slow due to long samples | Time/step in the initial run is too high | Reduce mixing ratio to 15%; apply early stopping based on select loss |
| Only 1 H100 available | — | Drop B13-Q, B15; run B10 immediately after B9 |
| ME fails to win at any ratio on gate | B12 | Shift the narrative to a controlled finding; consider submitting as a poster (CCIS) |
| Wide confidence intervals due to 19 articles | CI crosses 0 | Report passage-level bootstrap as well; state clearly in Limitations |