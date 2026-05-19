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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def walsh_fourier_coefficient(F, S):
        n = len(F[0])
        return sum((-1)**sum(S & T) for T in F) / len(F)
    
    def level_1_low_frequency_fraction(F):
        n = len(F[0])
        low_freq_sum = sum(walsh_fourier_coefficient(F, {i})**2 for i in range(n))
        total_freq_sum = sum(walsh_fourier_coefficient(F, S)**2 for S in range(1, 3))
        return low_freq_sum / total_freq_sum if total_freq_sum != 0 else 0
    
    def complexity_measure(lambda_value):
        return -math.log2(max(lambda_value, Fraction(1, len(F[0])))) if lambda_value > 0 else float('inf')
    
    def generate_random_monotone_dnf(n, s, term_widths):
        F = []
        for _ in range(s):
            T = set()
            while len(T) < term_widths:
                var = random.randint(0, n-1)
                if var not in T:
                    T.add(var)
            F.append(T)
        return F
    
    def k_clique_indicator(v):
        n = v * (v - 1) // 2
        F = []
        for i in range(n):
            T = set()
            u, v = divmod(i, v-1)
            T.add(u)
            T.add(v + u + 1)
            F.append(T)
        return F
    
    n_values = [16, 24, 32, 40]
    s_values = [10, 20, 40, 80, 160]
    term_widths = list(range(2, 7))
    
    results = []
    for n in n_values:
        for s in s_values:
            for _ in range(6):  # Ensure at least 30 instances per seed
                F = generate_random_monotone_dnf(n, s, term_widths)
                mu = complexity_measure(level_1_low_frequency_fraction(F))
                results.append({"n": n, "s": s, "mu": mu})
    
    for v in range(4, 9):
        F = k_clique_indicator(v)
        mu = complexity_measure(level_1_low_frequency_fraction(F))
        results.append({"v": v, "mu": mu})
    
    mean_mu = sum(result["mu"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["mu"] - mean_mu)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["mu"] <= 2 * math.log2(len(F[0]) + 2) + 4) / len(results)
    
    return {
        "metric_name": "complexity_measure",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"v={v}, mu={mu}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    mean_mu = sum(trial["metric_value"] for trial in trials) / len(trials)
    std_mu = math.sqrt(sum((trial["metric_value"] - mean_mu)**2 for trial in trials) / len(trials))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(trial["counterexample"]):
        v, mu = next((trial["v"], trial["mu"]) for trial in trials if trial["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"v={v}, mu={mu}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")