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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def matrix_mult(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def walsh_fourier_coefficient(F, S):
        n = len(F)
        sum_val = 0
        for i in range(n):
            if (i & S) == S:
                sum_val += (-1) ** bin(i).count('1')
        return sum_val / n
    
    def level_1_low_frequency_fraction(F):
        n = len(F)
        low_freq_sum = sum(walsh_fourier_coefficient(F, 1 << i) ** 2 for i in range(n))
        total_freq_sum = sum(walsh_fourier_coefficient(F, 1 << i) ** 2 for i in range(n + 1))
        return low_freq_sum / total_freq_sum
    
    def complexity_measure(mu):
        if mu <= 0:
            return float('inf')
        return -math.log2(max(mu, 1/len(F)))
    
    def generate_random_dnf(s, term_widths, n):
        F = [random.choice([0, 1]) for _ in range(n)]
        terms = []
        for _ in range(s):
            term = random.sample(range(n), random.choice(term_widths))
            terms.append(sorted(term))
        return F, terms
    
    def k_clique_indicator(v):
        n = v * (v - 1) // 2
        F = [0] * n
        for i in range(v):
            for j in range(i + 1, v):
                F[i * (v - 1) // 2 + j - i - 1] = 1
        return F
    
    def leaf_size(F):
        return sum(len(term) for term in F)
    
    n_values = [16, 24, 32, 40]
    s_values = [10, 20, 40, 80, 160]
    term_widths = range(2, 7)
    
    results = []
    for n in n_values:
        for s in s_values:
            F, terms = generate_random_dnf(s, term_widths, n)
            mu = complexity_measure(level_1_low_frequency_fraction(F))
            L = leaf_size(F)
            results.append({
                "n": n,
                "s": s,
                "L": L,
                "mu": mu
            })
    
    for v in range(4, 9):
        F = k_clique_indicator(v)
        mu = complexity_measure(level_1_low_frequency_fraction(F))
        results.append({
            "v": v,
            "mu": mu
        })
    
    mean_mu = sum(result["mu"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["mu"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["mu"] <= 2 * math.log2(result.get("L", 0) + 2) + 4) / len(results)
    
    return {
        "metric_name": "complexity_measure",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "random DNF with mu > 2*log2(L+2)+4"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_mu = sum(result["metric_value"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["metric_value"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"random DNF with mu > 2*log2(L+2)+4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")