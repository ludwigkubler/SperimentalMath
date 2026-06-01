The bootstrap is complete. The results tell a striking story I now write up honestly.

---

E3 RESOLUTION: PAIRED-BY-SEED CLUSTER BOOTSTRAP ON v4 §10 MECHANISM SLOPE

Setup. We loaded 180 rows from b2_mechanism.jsonl (n in {10,14,18,22,26,30}) and b2_dprime_mechanism.jsonl (n in {40,50,60}), 4 flag sets x 5 seeds (indexed k in 0..4 within each n). The cluster-bootstrap (B = 2000) resamples k with replacement and applies the SAME k-resample across all 9 ns (paired structure); for each resample we recompute mean log phi_c_drat per (flag, n), refit the OLS log-log slope on the 9 log-n values, and take slope_flag - slope_default. Full numerics live at /tmp/e3_bootstrap.txt on the server.

Headline result on the full 9-point fit.
- slope_norestart - slope_default: point +0.323, boot median +0.319, 95% percentile CI [+0.213, +0.435], excludes zero.
- slope_noinpr - slope_default:    point +0.137, boot median +0.123, 95% percentile CI [+0.070, +0.179], excludes zero.
- slope_noelim - slope_default:    point +0.030, boot median +0.029, 95% percentile CI [-0.005, +0.073], includes zero.

Taken at face value, the v4 §10 +0.323 finding for no-restart SURVIVES the paired bootstrap on the full 9-point fit (CI strictly positive). It also reveals a smaller but CI-positive no-inprocessing effect that v4 §10 underweights.

The honest qualification. The tied-cell diagnostic confirms the v4 panel's worry. For n in {10,14,18,22}, all 5 k-seeds give EXACTLY the same phi_c_drat across all four flags (20/20 ties for each non-default flag). For n=26 and n=30, only no-restart breaks a single tie (4/5 still tied). For no-inprocessing the first non-tied cell is n=40 (3/5 still tied) and the first majority-untied cell is n=50. No-eliminate is essentially flat: still 1/5 tied even at n=60. In other words, the entire mechanism signal lives in the rightmost 3 cells (n in {40,50,60}), and within those it concentrates at n=60.

Leave-n=60-out reweighting. Refitting on the 8 ns {10..50}:
- no-restart: point drops from +0.323 to +0.073, CI [+0.031, +0.111], still excludes zero but now four times smaller in magnitude;
- no-inprocessing: point +0.138 essentially unchanged, but CI explodes to [-0.048, +0.316] and no longer excludes zero (n=60 was holding the signal together);
- no-eliminate: point -0.003, CI [-0.006, +0.000], indistinguishable from null.

Leave-n>=50-out (b2 only, 6 ns {10..40}). no-restart slope difference is +0.128 with CI [0.000, +0.390] — barely touches zero at the lower bound, no longer cleanly excludes; the other two flags collapse to zero (no-eliminate is identically zero because every cell is tied through n=40).

Effective sample size. Cluster bootstrap on 5 seed-clusters and 9 (highly correlated) n-fits gives an effective DoF dominated by the 5 clusters (~4). The 9 log-n points are not independent — they share the same 5 underlying seed clusters — so headline CIs should be read with that caveat.

Honest verdict on v4 §10. The +0.323 no-restart finding is REAL on the full-range fit but FRAGILE: its magnitude is dominated by the n=60 cell (drops to +0.073 without it), the lower-range cells (n<=22) carry no information at all (20/20 ties), and the effective seed-cluster sample is only 5. The correct paper language is: "no-restart shows a positive log-log slope shift of +0.32 [+0.21, +0.43] on n in 10..60, but the effect is concentrated at the largest cell (n=60); excluding n=60 the shift drops to +0.07 [+0.03, +0.11], so the magnitude is not yet established and a push to n=70..100 is required before claiming a stable mechanism slope." The no-inprocessing effect should be reported as "suggestive (+0.14 [+0.07, +0.18] on full range) but CI crosses zero without n=60." The no-eliminate effect should be reported as null. v4 §10 therefore needs a downgrade in claim strength but NOT a full retraction: the slope-difference CI for no-restart does exclude zero on the full 9-point fit, contrary to the panel's worst-case reading; the panel was right that n=60 carries the signal.

Files: bootstrap output at /tmp/e3_bootstrap.txt on sec; script at /tmp/e3_bootstrap.py on sec and /tmp/e3_bootstrap_local.py locally.