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
    
    def generate_entangled_state(n):
        return [1] * n
    
    def compute_algebraic_hologram(state):
        # Simplified hologram computation for demonstration
        return sum(state) / len(state)
    
    def min_rank(hologram):
        # Simplified rank computation for demonstration
        return len(set(hologram))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        state = generate_entangled_state(n)
        hologram = compute_algebraic_hologram(state)
        rank = min_rank(hologram)
        ranks.append((n, rank))
    
    log_ns = [math.log2(n) for n in n_values]
    correlation_coefficient = calculate_spearman_correlation(ranks, log_ns)
    
    metric_name = "Spearman's rank correlation coefficient"
    metric_value = correlation_coefficient
    instances_tested = len(n_values)
    conjecture_holds = correlation_coefficient >= 0.8 and all(rank >= 0.5 * math.log2(n) for n, rank in ranks)
    counterexample = "" if conjecture_holds else "Spearman's coefficient < 0.8 or rank < 0.5 * log n"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_spearman_correlation(ranks, log_ns):
    n = len(ranks)
    rank_diffs = [(ranks[i][1] - log_ns[i]) for i in range(n)]
    rank_diff_sq_sum = sum(diff ** 2 for diff in rank_diffs)
    rank_diff_abs_sum = sum(abs(diff) for diff in rank_diffs)
    
    rho_numerator = n * rank_diff_sq_sum
    rho_denominator = (n - 1) * rank_diff_abs_sum ** 2
    
    return 1 - (6 * rho_numerator / rho_denominator)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Spearman's coefficient < 0.8 or rank < 0.5 * log n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")