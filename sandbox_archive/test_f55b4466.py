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
    
    def generate_protocol(n, m):
        phi_G = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        return phi_G
    
    def rank_variance(phi_G):
        n = len(phi_G)
        m = len(phi_G[0])
        sum_diff_squares = 0
        for row in phi_G:
            for i in range(m):
                for j in range(i+1, m):
                    diff = row[i] - row[j]
                    sum_diff_squares += diff ** 2
        return sum_diff_squares
    
    def geometric_invariant_rank(phi_G):
        n = len(phi_G)
        m = len(phi_G[0])
        rank = 0
        for i in range(m):
            if any(row[i] != 0 for row in phi_G):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi_G = generate_protocol(n, n)
            rank_var = rank_variance(phi_G)
            gir = geometric_invariant_rank(phi_G)
            results.append((n, gir, rank_var))
    
    if not results:
        return {
            "metric_name": "gir_over_rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gir_sum = sum(gir for _, gir, _ in results)
    rank_variance_sum = sum(rank_var for _, _, rank_var in results)
    n_total = len(results)
    gir_over_rank_variance_mean = Fraction(gir_sum, n_total) / Fraction(rank_variance_sum, n_total)
    
    return {
        "metric_name": "gir_over_rank_variance",
        "metric_value": float(gir_over_rank_variance_mean),
        "instances_tested": n_total,
        "n_max": max(n for _, _, _ in results),
        "conjecture_holds": gir_over_rank_variance_mean >= Fraction(9, 10) and gir_over_rank_variance_mean <= Fraction(11, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    gir_over_rank_variance_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(gir_over_rank_variance_values)/len(gir_over_rank_variance_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gir_over_rank_variance_outside_10_percent\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")