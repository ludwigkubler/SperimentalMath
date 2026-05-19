# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_random_monotone_dnf(n, s, term_widths):
    F = []
    for _ in range(s):
        T = set()
        while len(T) < term_widths:
            var = random.randint(0, n - 1)
            if var not in T:
                T.add(var)
        F.append(sorted(list(T)))
    return F

def generate_k_clique_indicator(v):
    k = math.isqrt(v)
    F = []
    for i in range(v):
        for j in range(i + 1, v):
            if (i, j) not in F and (j, i) not in F:
                F.append(sorted([i, j]))
    return F

def walsh_fourier_coefficient(F, S):
    s = len(F)
    n = max(max(T) for T in F)
    mu_hat_S = 0
    for T in F:
        if set(S).issubset(set(T)):
            mu_hat_S += (-1) ** len(S & T)
    return mu_hat_S / s

def level_1_low_frequency_fraction(F):
    n = max(max(T) for T in F)
    sum_level_1 = sum(walsh_fourier_coefficient(F, S)**2 for S in range(1, n + 1))
    sum_level_2 = sum(walsh_fourier_coefficient(F, S)**2 for S in range(2, n + 1))
    return sum_level_1 / sum_level_2

def complexity_measure(mu_F):
    if mu_F <= 0:
        return -math.inf
    return -math.log2(max(mu_F, 1/len(F)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Test ensemble (A): Random monotone DNFs
    results_A = []
    for n in [16, 24, 32, 40]:
        for s in [10, 20, 40, 80, 160]:
            term_widths = random.randint(2, 6)
            F = generate_random_monotone_dnf(n, s, term_widths)
            L_F = sum(len(T) for T in F)
            mu_F = complexity_measure(level_1_low_frequency_fraction(F))
            results_A.append({"n": n, "s": s, "L_F": L_F, "mu_F": mu_F})
    
    # Test ensemble (B): k-CLIQUE indicator
    results_B = []
    for v in [4, 5, 6, 7, 8]:
        F_v = generate_k_clique_indicator(v)
        mu_F_v = complexity_measure(level_1_low_frequency_fraction(F_v))
        results_B.append({"v": v, "mu_F_v": mu_F_v})
    
    # Evaluate the conjecture
    all_tests_passed_A = all(mu_F <= 2 * math.log2(L_F + 2) + 4 for _, _, L_F, mu_F in results_A)
    all_tests_passed_B = all(mu_F >= v / 8 for _, mu_F_v in results_B)
    
    return {
        "metric_name": "mu_F",
        "metric_value": sum(mu_F for _, _, _, mu_F in results_A) / len(results_A),
        "instances_tested": len(results_A) + len(results_B),
        "conjecture_holds": all_tests_passed_A and all_tests_passed_B,
        "counterexample": "" if all_tests_passed_A and all_tests_passed_B else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_mu_F = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu_F} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")