# Verified references for `paper/references.bib`

Checked on 2026-10-23. Every field in `references.bib` comes from one of these official records fetched that day:

- arXiv API (`export.arxiv.org/api/query?id_list=...`)
- ACL Anthology `.bib`
- OpenReview (`api2.openreview.net/notes/search`, venue note and its `_bibtex`)
- NeurIPS proceedings BibTeX (`proceedings.neurips.cc`)
- PMLR page (`proceedings.mlr.press`)
- Crossref (`api.crossref.org/works/<DOI>`)
- publisher pages (jcsce.vnu.edu.vn, taylorfrancis.com)
- Hugging Face cards and the HF API

Nothing was taken from memory.

Some sources could not be used:

- DBLP answered with a bot challenge (Anubis), and the exact-title OpenReview endpoint returned "ChallengeRequiredError". Neither was bypassed. Only OpenReview's public search endpoint was used.
- Full texts were read from the arXiv HTML version. The skill's `lay_van_ban_arxiv.py` wrote copies to the scratchpad, outside the repository. The versions read are listed at the end.

`bibtex`/`pdflatex` test: a scratch document with `llncs.cls`, `splncs04.bst` and `\nocite{*}` was compiled with MiKTeX. Results:

- 42 `\bibitem`s
- BibTeX `warning$ -- 0`
- pdflatex: no errors and no undefined references
- 2 harmless `Underfull \hbox` notices, caused by the long URLs in the notes of `bkai_news` and `wikimedia_wiki`

## 1. Entries

V = venue version cited, P = arXiv preprint cited, M = web or model card.

| Key | Identifier used | Checked | Date | Discrepancy / remark |
|---|---|---|---|---|
| ge2024icae | arXiv 2307.06945 (v4 "Final camera ready for ICLR'24"); OpenReview uREj4ZuGJE | V. Title and authors from arXiv; venue ICLR 2024 poster from OpenReview | 2026-10-23 | OpenReview lists the 2nd author as "Hu Jing"; arXiv has "Jing Hu" (arXiv form used) |
| li2024_500x | ACL Anthology 2025.acl-long.1219 (arXiv 2408.03094) | V. Anthology .bib | 2026-10-23 | **Published at ACL 2025 (long), so year = 2025.** The arXiv comment does not mention this; found through Crossref, bib taken from the Anthology |
| cheng2024xrag | NeurIPS 2024 proceedings (hash c5cf13bf…), DOI 10.52202/079017-3476; arXiv 2405.13792 | V. Proceedings BibTeX: vol. 37, pp. 109487–109516 | 2026-10-23 | none |
| liu2025sac | OpenReview 8Pi6Du0n7F; arXiv 2510.08907 | V. Authors from arXiv; venue from OpenReview (ICLR 2026 poster) | 2026-10-23 | **Venue is ICLR 2026, so year = 2026.** The arXiv comment says only "23 pages,10 figures". OpenReview spells the last author "JingBo Zhu"; arXiv has "Jingbo Zhu" (arXiv form used) |
| xu2026latentpress | arXiv 2609.01507 (v3) | P. arXiv API | 2026-10-23 | **The first author is Yuanda Xu; Zhengze Zhou is 2nd author.** Key renamed from `zhou2026latentpress` to `xu2026latentpress` on 2026-10-23. No venue found |
| fallahpour2026memorilla | arXiv 2610.21375 (v1, 2026-10-15) | P. arXiv API (title, 7 authors) and abs page | 2026-10-25 | Added 2026-10-25 for Future Work (checklist A21). Abstract: documents encoded once, compressed into 16 query-dependent memory tokens for a frozen LLM. Comment field gives only a project website; no venue |
| rahman2026cmc | arXiv 2609.25537 (v1) | P. arXiv API | 2026-10-23 | No venue found |
| deng2024gist | ACL Anthology 2025.acl-long.241 (arXiv 2412.17483) | V. Anthology .bib, pp. 4861–4879 | 2026-10-23 | **Published at ACL 2025 (long), so year = 2025** |
| laguna2026cartridges | arXiv 2609.35621 (v1) | P. arXiv API | 2026-10-23 | No venue found |
| mu2023gist | NeurIPS 2023 proceedings (hash 3d77c6dc…), DOI 10.52202/075280-0848; OpenReview 2DtxPCL3T5; arXiv 2304.08467 | V. Proceedings: vol. 36, pp. 19327–19352 | 2026-10-23 | The proceedings bib names the 2nd author "Li, Xiang"; OpenReview and arXiv both have "Xiang Lisa Li" (used) |
| louis2025oscar | OpenReview ideKAUWvFE (ICLR 2026 poster); arXiv 2504.07109 | V. OpenReview bib; its abstract opens with the same text as arXiv v2 | 2026-10-23 | **Published at ICLR 2026 under a different title, "OSCAR: Online Soft Compression for RAG"** (arXiv: "OSCAR: Online Soft Compression And Reranking"). Year = 2026. Found through the AdaMem reference list, then confirmed on OpenReview. arXiv comment empty |
| louis2025pisco | ACL Anthology 2025.findings-acl.800 (arXiv 2501.16075) | V. Anthology .bib | 2026-10-23 | **Venue: Findings of ACL 2025** (arXiv comment empty) |
| sakhno2026adamem | arXiv 2609.22100 (v1) | P. arXiv API | 2026-10-23 | No venue found |
| haghifam2026sedem | arXiv 2608.00311 (v2) | Accepted-only. Comment "Accepted at EMNLP 2026 Main Conference" | 2026-10-23 | **FLAG: not in the ACL Anthology yet** (`aclanthology.org/events/emnlp-2026/` returned 404). Entry is `@inproceedings` with booktitle "EMNLP 2026 (Main Conference)" and note "Accepted; to appear. arXiv:2608.00311". Update when the proceedings appear |
| xie2026lensvlm | arXiv 2605.07019 (v4, 2026-10-09) | Accepted-only. Comment "Accepted to NeurIPS 2026" | 2026-10-23 | **FLAG: no proceedings yet**, and no OpenReview title match. Booktitle "NeurIPS 2026" with note "Accepted; to appear. arXiv:2605.07019". Primary category cs.CV |
| jiang2023llmlingua | ACL Anthology 2023.emnlp-main.825 (arXiv 2310.05736) | V. Anthology .bib | 2026-10-23 | none |
| jiang2024longllmlingua | ACL Anthology 2024.acl-long.91 (arXiv 2310.06839) | V. Anthology .bib | 2026-10-23 | ACL 2024 (long) confirmed |
| pan2024llmlingua2 | ACL Anthology 2024.findings-acl.57 (arXiv 2403.12968) | V. Anthology .bib | 2026-10-23 | none |
| li2023selective | ACL Anthology 2023.emnlp-main.391; arXiv 2310.06201 | V. Anthology .bib | 2026-10-23 | Author order differs: arXiv has Li, Dong, **Lin, Guerin**; the Anthology has Li, Dong, **Guerin, Lin** (Anthology used). The arXiv id was not in the task list; found by an arXiv title search |
| xu2024recomp | OpenReview mlJLVigNHp (ICLR 2024 poster); arXiv 2310.04408 | V. OpenReview bib | 2026-10-23 | **ICLR title differs from arXiv:** "…Retrieval-Augmented LMs with **Context** Compression and Selective Augmentation" (ICLR title used) |
| cao2024qgc | ACL Anthology 2024.acl-long.685 (arXiv 2406.02376) | V. Anthology .bib | 2026-10-23 | none |
| lukauskas2026lost | arXiv 2608.26175 (v1) | P. arXiv API | 2026-10-23 | No venue found |
| lajewska2025information | ACL Anthology 2025.findings-emnlp.949 (arXiv 2503.19114) | V. Anthology .bib | 2026-10-23 | The Anthology prints "Marquez, Lluis" without diacritics; arXiv prints "Lluís Màrquez" (arXiv spelling used, as `M{\`a}rquez, Llu{\'i}s`). "Anna John, Neha" is split as the Anthology splits it |
| kim2025kvzip | NeurIPS 2025 proceedings (hash f4eaa4b8…), DOI 10.52202/085713-5585; OpenReview JFygzwx8SJ (oral) | V. Proceedings: pp. 167563–167591 | 2026-10-23 | The proceedings volume field reads "38, Main Conference"; `volume = {38}` used |
| lee2024readagent | PMLR v235 lee24c (arXiv 2402.09727) | V. PMLR BibTeX: pp. 26396–26415 | 2026-10-23 | ICML 2024 confirmed. The arXiv comment gives only a website |
| li2024selfroute | ACL Anthology 2024.emnlp-industry.66 (arXiv 2407.16833) | V. Anthology .bib | 2026-10-23 | EMNLP 2024 Industry Track confirmed |
| joren2025sufficient | OpenReview Jjr2Odj8DJ (ICLR 2025 poster); arXiv 2411.06037 | V. OpenReview bib | 2026-10-23 | ICLR 2025 confirmed. The arXiv comment is empty |
| lester2021prompt | ACL Anthology 2021.emnlp-main.243 (arXiv 2104.08691) | V. Anthology .bib | 2026-10-23 | none |
| hinton2015distilling | arXiv 1503.02531 (v1) | P. arXiv API | 2026-10-23 | arXiv comment: "NIPS 2014 Deep Learning Workshop", a non-archival workshop, so cited as an arXiv preprint |
| loshchilov2019adamw | OpenReview Bkg6RiCqY7; arXiv 1711.05101 | V. OpenReview bib (booktitle "International Conference on Learning Representations", 2019) | 2026-10-23 | none |
| yang2025gdn | OpenReview r8H7xhYPwz (ICLR 2025 poster); arXiv 2412.06464 | V. OpenReview bib | 2026-10-23 | none |
| wolf2020transformers | ACL Anthology 2020.emnlp-demos.6 | V. Anthology .bib (22 authors) | 2026-10-23 | none |
| qwen35 | HF model card `Qwen/Qwen3.5-2B` (README, sha 15852e8c…); blog `https://qwen.ai/blog?id=qwen3.5` (HTTP 200) | M | 2026-10-23 | **No Qwen3.5 (text LLM) technical report on arXiv.** Searches `ti:"Qwen3.5" AND ti:"Technical Report"` and `au:"Qwen Team" AND ti:Qwen3.5` found only "Qwen3.5-Omni Technical Report" (2604.15804), which is a different model. The model card's "Citation" section asks for `@misc{qwen3.5, title={{Qwen3.5}: Towards Native Multimodal Agents}, author={{Qwen Team}}, month={February}, year={2026}, url=...blog}`. That citation is used, with the model-card URL and access date in `note`. The card also gives the facts the paper may use: 2B, hidden dimension 2048, 24 layers, layout 6 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN)), 262,144 native context, Apache-2.0 |
| robertson2009bm25 | DOI 10.1561/1500000019 | V. Crossref: journal "Foundations and Trends in Information Retrieval", vol./no./pages written into the .bib by script from the Crossref JSON (vol. 4, no. 1–2, pp. 1–174), 2009 | 2026-10-23 | Crossref registrant/publisher is "Emerald". The DOI redirects to emerald.com (HTTP 403 for scripts), and the redirect URL path also encodes vol. 4 / issue 1-2 / p. 1. Please eyeball the volume and issue once on the publisher page in a browser |
| efron1993bootstrap | DOI 10.1201/9780429246593 (Chapman and Hall/CRC) | V. Crossref and the taylorfrancis.com landing page (citation_publisher "Chapman and Hall/CRC", citation_publication_date 1994/05/15) | 2026-10-23 | **This official record gives year 1994, not 1993.** A second Crossref record exists: DOI 10.1007/978-1-4899-4541-9, publisher "Springer US", 1993, ISBN 978-0-412-04231-7, authors "Bradley Efron, Robert J. Tibshirani". Its DOI resolves to a Springer 404 page, so it was not used. Key kept as `efron1993bootstrap` |
| petrov2023tokenizer | NeurIPS 2023 proceedings (hash 74bb24dc…), DOI 10.52202/075280-1608; OpenReview 78yDLKi95p; arXiv 2305.15425 | V. Proceedings: vol. 36, pp. 36963–36990 | 2026-10-23 | Proceedings and OpenReview have "Philip Torr"; arXiv has "Philip H. S. Torr" (proceedings form used). **No HTML full text:** `arxiv.org/html/2305.15425` returns 404 and the ar5iv conversion failed (see section 4) |
| nguyen2020phobert | ACL Anthology 2020.findings-emnlp.92 | V. Anthology .bib, pp. 1037–1042 (authors as printed: "Nguyen, Dat Quoc; Tuan Nguyen, Anh") | 2026-10-25 | Added 2026-10-25 for the PhoBERT sentence-selector baseline (checklist A12); editors omitted as in the other Anthology entries |
| nguyen2020viquad | ACL Anthology 2020.coling-main.233 | V. Anthology .bib (authors as printed: "Van Nguyen, Kiet; Nguyen, Duc-Vu; Gia-Tuan Nguyen, Anh; Nguyen, Ngan Luu-Thuy") | 2026-10-23 | none |
| nguyen2022vlsp | DOI 10.25073/2588-1086/vnucsce.340 (arXiv 2203.11400 v3 metadata carries this DOI) | V. Crossref and the journal page jcsce.vnu.edu.vn/…/view/340: VNU J. Sci.: Comput. Sci. Commun. Eng. **38(2)**, published 2022-12-16 | 2026-10-23 | **The published journal version is cited.** No page numbers in Crossref or on the journal page, so pages are omitted. Author forms differ: Crossref "Kiet Nguyen" (used), arXiv "Kiet Van Nguyen", journal page "Nguyen Van Kiet". The UIT-ViQuAD 2.0 card asks for this paper (section 5) |
| lewis2020mlqa | ACL Anthology 2020.acl-main.653 | V. Anthology .bib | 2026-10-23 | none |
| bandarkar2024belebele | ACL Anthology 2024.acl-long.44 (arXiv 2308.16884; its journal_ref and DOI match) | V. Anthology .bib | 2026-10-23 | none |
| nguyen2019vnds | DOI 10.1109/nics48868.2019.9023886 | V. Crossref: 2019 6th NAFOSTED Conference on Information and Computer Science (NICS), IEEE, pp. 375–380, Hanoi, 12–13 Dec 2019 | 2026-10-23 | Crossref splits the 4th author as given "Nguyen Xuan", family "Hoai" (kept as `Hoai, Nguyen Xuan`) |
| bkai_news | arXiv 2403.01616 (v2), requested by the HF card `bkai-foundation-models/BKAINewsCorpus` (sha 78332188…) | P. arXiv API | 2026-10-23 | **The card asks for this citation**, so it is used instead of a @misc; the dataset URL and access date go in `note`. arXiv prints names family-first ("Nguyen Quang Duc", …). They are encoded as `Nguyen, Quang Duc`, so splncs04 prints "Nguyen, Q.D." |
| wikimedia_wiki | HF dataset `wikimedia/wikipedia` (config `20231101.vi`; API sha b04c8d1c…) | M. The card's "Citation Information" gives `@ONLINE{wikidump, author="Wikimedia Foundation", title="Wikimedia Downloads", url="https://dumps.wikimedia.org"}` | 2026-10-23 | Used as @misc with that author, title and URL. The card gives no year, so none is added; the dump date (20231101), HF URL and access date are in `note`. Licence per card: CC BY-SA 3.0 and GFDL |

### UNVERIFIED

No bibliographic entry is unverified; all 42 were matched to an official record. Three points are still open:

1. **Petrov et al., Vietnamese token premium.** The paper text was not read, because there is no arXiv HTML and the skill forbids PDF. See section 4.
2. **efron1993bootstrap year.** The official records conflict: CRC DOI 1994, dead Springer DOI 1993. Decide which to keep.
3. **haghifam2026sedem / xie2026lensvlm.** Accepted-only. Re-check when the EMNLP 2026 and NeurIPS 2026 proceedings appear.

Searches that found no venue: Crossref bibliographic search and OpenReview title search for LatentPress, CMC, Cartridges++, AdaMem, Lost in Compression and LensVLM. DBLP was blocked.

## 2. Numeric claims

Method: string search in the arXiv HTML text, then reading the surrounding passage. Each quote is under 15 words. All quotes were re-checked to occur verbatim in the normalised source text with a small script (0 misses).

### 1. LatentPress (2609.01507v3): **CONFIRMED**

- Writer = the reader's bottom 2 layers, frozen and deep-copied: "borrows the reader's bottom two transformer layers to encode context before pooling" [App. C.2]. App. A.1 says the same in its own words: the bottom L = 2 layers of the frozen Qwen2.5-7B-Instruct decoder, deep-copied.
- Adapter: a linear d×d adapter "initialized to the identity, so the writer begins close to the raw token embeddings" [App. A.1].
- Nuance: the adapter output is fused with the embeddings, "where they are combined with the original token embeddings before pooling" [§2.1].
- Pooling: "uniform mean pooling" [App. B.2].
- Injection: "injected through the decoder's input-embedding interface" (`inputs_embeds`) [App. A.1].
- Loss: L = L_rec + λ·L_fkl, where L_rec is teacher-forced cross-entropy and L_fkl = KL(p_full ‖ p_comp), with λ = 1.0 [§2.3, Eq. 3–5; Table 6]. Quote: "the forward-KL term distills the full-context behavior into the writer" [§2.3].
- Accuracy: Table 4 "In-domain LatentPress on LongBench-QA English" [§4.2], Qwen2.5-7B.
  - raw context 43.80
  - f4: 49.06 ± 2.30
  - f8: 43.77 ± 2.83
  - f16: 37.78 ± 3.46
  - values are mean ± std over five seeds
- Parameters: "Only the writer head is trained, and its size is backbone-dependent" [§2.3]. The paper gives 4.196 M for **Qwen3-1.7B**, 16.781 M for **Qwen3-8B**, 12.849 M for Qwen2.5-7B and 26.220 M for Qwen2.5-14B.
  - **Precision note:** the paper attributes these counts to backbones and never prints "d = 2048 / 4096".
  - Saying d = 2048 and d = 4096 is our own arithmetic (d² + d bias: 2048² + 2048 = 4,196,352 and 4096² + 4096 = 16,781,312).
  - Write it as "4.196 M for Qwen3-1.7B" rather than as a d value.

### 2. AdaMem (2609.22100v1), Table 1: **CONFIRMED**

- Match (%) at 16×: PISCO HotpotQA **38.4**, NQ **58.9**; OSCAR HotpotQA **44.1**, NQ **62.8**.
- Table 1 caption: "Match (%) performance on six QA benchmarks with 25 retrieved documents".
- Same setup: "we train PISCO, OSCAR, and AdaMem using identical data splits, hyperparameters, and training stages" [Experiments, "Baselines"].
- Wording: "PISCO uses query-independent passage compression"; OSCAR is described as "query-conditioned" [same paragraph].

### 3. Łajewska et al. (2503.19114v2), Table 7: **CONFIRMED**

- Caption: "Fraction of entities preserved in the reconstructed context using xRAG and PISCO models" [Table 7, §4.3].
- xRAG, unseen data, 1 encoding per sample: DATE **0.22**, CARD. **0.26** (Avg 0.28, PERSON 0.31, GPE 0.39, ORG 0.32).
- Caveats for the wording:
  - This measures entities kept in the *reconstructed* context.
  - On "seen" data, xRAG keeps DATE 0.24 and CARD. 0.38.
  - With 1 encoding per sentence (unseen), xRAG keeps DATE 0.14 and CARD. 0.13.

### 4. Lost in Compression (2608.26175v1): **CONFIRMED**

- Abstract: "at 0.33 English retains 57-62% of normalized context utilization" and "Lithuanian retains 10-24% and Chinese essentially none".
- Table 1 (LLMLingua-2; GPT-5.4-mini / Claude Haiku 4.5; ρ = 0.33):
  - EN 0.57 / 0.62
  - LT 0.10 / 0.24
  - ZH −0.03 / 0.26
- Text: "Chinese drops below the no-context anchor" (U = −0.03, GPT) [§4].
- **Nuance:** "Chinese near 0" holds for GPT-5.4-mini only; for Claude Haiku it is 0.26. The audited compressor is LLMLingua-2 (an extractive compressor).
- **Vietnamese: NO.** The languages are EN plus PL, LV, FI, ET, LT, UK, ZH, AR, HI (Table 1). There are 0 hits for "Vietnam" or "VI" in the text.

### 5. Self-Route (2407.16833v2): **WRONG as worded (location / values)**

- The numbers 46.83 vs 47.04 are **not in Table 1**. They appear only in the text of §4.3: "GPT-4O uses only 61% tokens while achieving comparable performance (46.83) with LC (47.04)".
- **Table 1** ("Results of Gemini-1.5-Pro, GPT-3.5-Turbo, and GPT-4O using the Contriever retriever"), GPT-4O, Avg column:
  - LC (row 2-1) **48.67**
  - Self-Route (row 2-3) **48.89**
  - token % (row 2-5) **61.40**
- The paper is internally inconsistent here. Either cite "§4.3: 46.83 vs 47.04 with 61% of tokens", or cite "Table 1: 48.89 vs 48.67 with 61.4% of tokens", but do not mix the two.

### 6. QGC (2406.02376v2), Table 2: **CONFIRMED**

- Caption: "ablation study on NaturalQuestions test set, where the target LLM is LongChat-13B".
- Values:
  - QGC 69.19
  - w/o query-guided context encoder 50.36
  - w/o query-guided pooling layer 55.34
  - (w/o reviewing layer 64.14; w/o dynamic strategy 62.15)
- The pooling ablation is mean pooling: "directly replace the weighted sum of token representations" … "with their mean representation".
- The encoder ablation: "the query and document are independently encoded" [§4, "Ablation Study"].

### 7. KVzip (2505.23416v2): **CONFIRMED**

- "suffer from performance degradation even at a 90% cache budget ratio under multi-query scenarios" [Abstract].
- §4.2 also notes that baselines "degrade notably at 90% retention".

### 8. SAC (2510.08907v4): **CONFIRMED**

- "the cosine similarity quickly approaches zero, suggesting that the two tasks are largely orthogonal" [§5.1 "AE Analysis", Fig. 9].
- The figure shows AE-loss vs LM-loss gradient cosine similarity.

## 3. Descriptive claims

### 9. Selective Context (2310.06201v1, = li2023selective): **CONFIRMED**

- "evaluates informativeness of lexical units (i.e., tokens, phrases, or sentences) with self-information" [§1].
- "We use smaller base causal language model for self-information computing" [§4.4]. The models are LLaMA-7B, or GPT-3 "curie" for the OpenAI family.

### 10. LLMLingua (2310.05736v2): **CONFIRMED**

- "a budget controller to maintain semantic integrity under high compression ratios" and "a token-level iterative compression algorithm" [Abstract].
- Algorithm 1 input: "A small language model".
- "allows for up to 20x compression with little performance loss" [Abstract].
- Omitted from the claim: a third component, instruction-tuning-based distribution alignment between the small LM and the target LLM.

### 11. LongLLMLingua (2310.06839v2): **CONFIRMED**

- "We propose a question-aware coarse-to-fine compression method" [§1, contribution 1; method §4.1].
- Other parts: document reordering, dynamic compression ratios, subsequence recovery.

### 12. LLMLingua-2 (2403.12968v2): **CONFIRMED**

- "binary token classification problem" (preserve or discard) [§4].
- Data: "derive knowledge from an LLM (GPT-4) to compress the prompts", built from "pairs of original texts from MeetingBank" [§1].
- Encoders: "smaller models such as XLM-RoBERTa-large and mBERT" [Abstract]. There are two variants; XLM-RoBERTa-large is the main one.

### 13. RECOMP (2310.04408v1): **CONFIRMED**

- "an extractive compressor which selects useful sentences from retrieved documents" and "an abstractive compressor which generates summaries" [Abstract].

### 14. Gist tokens (2304.08467v3): **CONFIRMED**

- "by simply modifying Transformer attention masks to encourage prompt compression" [Abstract].
- "no additional cost over standard instruction finetuning" [Abstract].

### 15. ICAE (2307.06945v4): **CONFIRMED**

- "The encoder of the ICAE is a LoRA-adapted LLM" [Fig. 3, §2.1].
- "introducing about 1% additional parameters" [Abstract].
- "pretrained using both autoencoding and language modeling objectives", then "fine-tuned on instruction data" [Abstract].

### 16. 500xCompressor (2408.03094v1): **PARTLY WRONG**

- KV values: CONFIRMED. "500xCompressor uses the K V values for the compressed tokens" [§2.1].
- Compression range: CONFIRMED. 6×–480×.
- Extra parameters: **WRONG. The paper says ≈0.25%, not 0.3%:** "introduces approximately 0.25% additional parameters and achieves compression ratios ranging from 6x to 480x" [Abstract].
- The ACL 2025 version was not read.

### 17. xRAG (2405.13792v2): **CONFIRMED**

- "the modality bridge is the only trainable component" [Abstract]. The retriever and the LLM are frozen.
- One token: the title says "with One Token". The projector is a two-layer MLP [§3.4].

### 18. Deng et al. (2412.17483v1): **CONFIRMED**

- "lost by the boundary, lost if surprise, and lost along the way" [Abstract; §4.2].

### 19. CMC (2609.25537v1): **CONFIRMED**, with wording fixes

- Encoder: a separate trainable ContextEncoder (GPT2-Large or OPT-1.3B/2.7B, Table 4) with "fixed placeholder tokens bounded by special <MEM> and </MEM> tokens" [§2.1].
- Bridge: MemoryBridge, "a norm-calibrated two-layer MLP" [§1, §2.3].
- The paper says **"Phase-2"**, not "stage-2". The Phase-2 loss is L₂ = L_CE + λ_KL·L_KL + λ_CL·L_CL [Eq. 10]. Quote: "via cross-entropy, KL divergence, and contrastive memory-answer alignment losses" [§1].
- Weights: λ_KL = 0.5 and λ_CL = 0.1 (Table 4). The decoder is frozen.

### 20. Cartridges++ (2609.35621v1): **CONFIRMED**

- There are two separate variants:
  - data mixing (C++^D): "allocates a small fraction of training Q/As to queries outside the reference long document" [Abstract];
  - an inference-time relevance router (C++^R), which uses a kNN classifier: "router as our main variant for simplicity" [§4].

### 21. PISCO (2501.16075v1): **CONFIRMED**

- "PISCO requires no pretraining or annotated data, relying solely on sequence-level knowledge distillation" [Abstract].
- On "query-agnostic": PISCO never uses that word, but its compressor input is only the document plus memory tokens. The memory-token set "is appended to each document" [§3.2]. AdaMem calls it "query-independent passage compression".

### 22. Łajewska et al. (2503.19114v2): what remedy?

The remedy they **implement and evaluate** is controlling the compression granularity of xRAG:

- one token per sentence instead of per context;
- sentence-level pre-training, then sentence-level fine-tuning ("w/ Sentence PT + FT");
- or two-step pre-training ("w/ Two-Step PT + FT") [§5].

Quote: "improve one soft prompting method by controlling compression granularity" [Abstract].

Keeping entities and numbers as hard tokens appears **only as a future direction**: "hard prompts preserve key details (e.g., numbers, names)" [§6 "Hybrid Soft-Hard Prompting"]. Cite it as "they suggest" (proposed), not as a method they tested.

### 23. SeDeM (2608.00311v2): **CONFIRMED**

- "Our compression is query-independent; the query only affects scoring and selection" [§3.2].
- A learned top-K selector (trained with block-level evidence supervision) feeds a decompressor that "decompresses only the selected blocks for decoder conditioning" [Abstract].

### 24. Sufficient Context (2411.06037v3): **CONFIRMED**

- Autorater: Gemini 1.5 Pro (1-shot). "It achieves 93% accuracy, outperforms other methods" [§3.2, Table 1].
- Range: "we believe this mostly explains the 35-62% correct rate with insufficient context" [§4.3].

### Does each paper's experiments include Vietnamese?

Only from what was read. Method: full-text search for "Vietnam", "vie_" and "VI", then reading each hit.

| Key | Vietnamese? | Evidence |
|---|---|---|
| ge2024icae, li2024_500x, cheng2024xrag, liu2025sac, xu2026latentpress, rahman2026cmc, deng2024gist, laguna2026cartridges, mu2023gist, louis2025oscar, sakhno2026adamem, haghifam2026sedem, xie2026lensvlm, jiang2023llmlingua, li2023selective, xu2024recomp, cao2024qgc, kim2025kvzip, lee2024readagent, li2024selfroute, joren2025sufficient, lester2021prompt, hinton2015distilling, loshchilov2019adamw, yang2025gdn | no | 0 mentions in the arXiv full text |
| jiang2024longllmlingua | no | Its only hit is an example question ("What was the Vietnam War ?"), not a language |
| pan2024llmlingua2 | no | The multilingual appendix (App. J) uses Chinese LongBench only |
| louis2025pisco | no | "We choose a latin language (french) as well as Korean and Russian" [§4.4] |
| lukauskas2026lost | no | 9 non-English languages, none Vietnamese |
| lajewska2025information | no | "our analysis focuses exclusively on English benchmarks" [Limitations] |
| petrov2023tokenizer | not read in the paper | The project-page data includes Vietnamese (see section 4) |
| wolf2020transformers, robertson2009bm25, efron1993bootstrap | not checked | Full text not read; not experimental in the relevant sense |
| nguyen2020viquad | yes | Vietnamese MRC dataset (Anthology abstract) |
| nguyen2022vlsp | yes | UIT-ViQuAD 2.0, Vietnamese MRC shared task |
| lewis2020mlqa | yes | "MLQA contains QA instances in 7 languages, … Vietnamese …" (Anthology abstract) |
| bandarkar2024belebele | yes | `vie_Latn` is in the language table and the result tables |
| nguyen2019vnds | yes | Vietnamese summarisation dataset, per the title (abstract not read) |
| bkai_news | yes | Vietnamese news corpus (card) |
| wikimedia_wiki | yes | Config `20231101.vi` |
| qwen35 | not stated | The card claims 201 languages and dialects but never names Vietnamese |

## 4. Petrov et al. (petrov2023tokenizer): Vietnamese premium

**The paper text could not be checked.** `https://arxiv.org/html/2305.15425` and the v1/v2 URLs return 404, the ar5iv page says "Conversion to HTML had a Fatal error", and the skill rule forbids using the PDF. So it is **NOT VERIFIED** whether the paper prints a Vietnamese premium, or where.

What could be checked is the authors' project page, `aleksandarpetrov.github.io/tokenization-fairness`, which the arXiv comment links. Its data file `assets/tokenization_lengths_validated.csv` (2000 FLORES-200 sentences) has a "Vietnamese" row.

Vietnamese / English token-count ratios **computed by us** from that CSV (not numbers printed in the paper):

| Tokenizer | Ratio |
|---|---|
| GPT-2 / r50k / p50k | 4.54 |
| LLaMA (1) | 2.92 |
| cl100k_base (GPT-3.5/4) | 2.45 |
| mT5 | 1.95 |
| Qwen (2023 tokenizer, not Qwen3.5) | 1.41 |
| ByT5 | 1.39 |
| BLOOM | 1.27 |
| XLM-R | 1.18 |
| PhoBERT | 0.83 |

Recommendation: do not cite a specific Vietnamese number to Petrov et al. unless someone reads the PDF table. Either cite the paper only for the general finding (its abstract, as reproduced on the project page, says "differences up to 15 times in some cases"), or measure the premium with the Qwen3.5 tokenizer on our own data.

(Lost in Compression is a related source: it reports 1.3–1.8× more o200k tokens for its nine languages and up to 4.5× under the Qwen2.5 tokenizer for Hindi, but it has no Vietnamese.)

## 5. Which citation does the UIT-ViQuAD 2.0 card ask for?

The Hugging Face card `taidng/UIT-ViQuAD2.0` is a community re-upload ("The HF version…"), not the official release. Its "Citation Information" asks for two papers:

1. the original dataset paper, COLING 2020 (`nguyen-etal-2020-vietnamese`, i.e. our `nguyen2020viquad`);
2. "Shared task where version 2.0 was published": the VNU Journal article with DOI 10.25073/2588-1086/vnucsce.340 (our `nguyen2022vlsp`).

Both are in the .bib, so cite both when using UIT-ViQuAD 2.0. The card directs dataset questions to `nlp.uit.edu.vn/datasets`, which was not opened.

## 6. Source versions read (arXiv HTML; scratchpad copies, not in the repo)

| arXiv id | Version | Version date |
|---|---|---|
| 1503.02531 | v1 | 2015-03-09 |
| 1711.05101 | v3 | 2019-01-04 |
| 2104.08691 | v2 | 2021-09-02 |
| 2203.11400 | v3 | 2022-04-04 |
| 2304.08467 | v3 | 2024-02-12 |
| 2307.06945 | v4 | 2024-05-08 |
| 2308.16884 | v2 | 2024-07-25 |
| 2310.04408 | v1 | 2023-10-06 |
| 2310.05736 | v2 | 2023-12-06 |
| 2310.06201 | v1 | 2023-10-09 |
| 2310.06839 | v2 | 2024-08-12 |
| 2402.09727 | v3 | 2024-07-22 |
| 2403.12968 | v2 | 2024-08-12 |
| 2405.13792 | v2 | 2024-12-09 |
| 2406.02376 | v2 | 2024-06-17 |
| 2407.16833 | v2 | 2024-10-17 |
| 2408.03094 | v1 | 2024-08-06 |
| 2411.06037 | v3 | 2025-04-23 |
| 2412.06464 | v3 | 2025-03-06 |
| 2412.17483 | v1 | 2024-12-23 |
| 2501.16075 | v1 | 2025-01-27 |
| 2503.19114 | v2 | 2025-10-10 |
| 2504.07109 | v2 | 2026-03-04 |
| 2505.23416 | v2 | 2025-09-30 |
| 2510.08907 | v4 | 2026-03-11 |
| 2605.07019 | v4 | 2026-10-09 |
| 2608.00311 | v2 | 2026-09-10 |
| 2608.26175 | v1 | 2026-07-27 |
| 2609.01507 | v3 | 2026-10-10 |
| 2609.22100 | v1 | 2026-08-12 |
| 2609.25537 | v1 | 2026-09-22 |
| 2609.35621 | v1 | 2026-09-28 |

Not available as HTML: 2305.15425.
