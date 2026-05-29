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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def minterms(f, n):
        return [i for i in range(2**n) if f[i] == 1]
    
    def monomial_ideals(mints):
        ideals = set()
        for mint in mints:
            ideal = {mint}
            for j in range(len(mint)):
                if mint[j] == 1:
                    new_mint = mint[:j] + (0,) + mint[j+1:]
                    if new_mint not in ideals:
                        ideal.add(new_mint)
            ideals.add(frozenset(ideal))
        return ideals
    
    def dynkin_diagram(n):
        if n == 2: return {0, 1}
        elif n == 3: return {0, 1, 2}
        elif n == 4: return {0, 1, 2, 3}
        else: return set()
    
    def spearman_rank_correlation(x, y):
        if len(x) != len(y): return None
        x_rank = {x[i]: i for i in range(len(x))}
        y_rank = {y[i]: i for i in range(len(y))}
        n = len(x)
        sum_d1_sq = sum((x_rank[x[i]] - y_rank[y[i]])**2 for i in range(n))
        sum_d2_sq = sum((i - (n-1)/2)**2 for i in range(n))
        return 1 - (6 * sum_d1_sq) / (n * (n**2 - 1)) if sum_d2_sq != 0 else None
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        mints = minterms(f, n)
        ideals = monomial_ideals(mints)
        vertices = len(dynkin_diagram(n))
        results.append((len(ideals), vertices))
    
    if not results: return {"metric_name": "Spearman Rank Correlation", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "empty_results"}
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = spearman_rank_correlation(x, y)
    
    return {"metric_name": "Spearman Rank Correlation", "metric_value": correlation if correlation is not None else 0.0, "instances_tested": len(results), "conjecture_holds": correlation >= 0.7, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    all_results = []
    total_metric_value = 0.0
    count_supporting_conjecture = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.append(trial_result["metric_value"])
        if trial_result["conjecture_holds"]:
            count_supporting_conjecture += 1
        total_metric_value += trial_result["metric_value"]
    
    mean_metric_value = sum(all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in all_results) / len(all_results))
    support_fraction = count_supporting_conjecture / len(seeds)
    
    if all(r is not None for r in all_results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(r is None for r in all_results):
        RESULT = "INCONCLUSIVE" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")