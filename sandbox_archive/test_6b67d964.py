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
    
    def generate_protocol(n):
        vertices = list(range(n))
        edges = []
        for v in vertices:
            for u in range(v + 1, n):
                if random.choice([True, False]):
                    edges.append((v, u))
        return vertices, edges
    
    def deligne_lusztig_parameters(G, V):
        vertices, edges = G
        n = len(vertices)
        dl_param = 0
        for v in vertices:
            neighbors = [u for u in vertices if (v, u) in edges or (u, v) in edges]
            dl_param += len(neighbors)
        return Fraction(dl_param, n * (n - 1))
    
    def communication_complexity_rank(G):
        vertices, edges = G
        rank = 0
        for v in vertices:
            neighbors = [u for u in vertices if (v, u) in edges or (u, v) in edges]
            rank += len(neighbors)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        vertices, edges = generate_protocol(n)
        dl_param = deligne_lusztig_parameters((vertices, edges), vertices)
        r_pi = communication_complexity_rank((vertices, edges))
        results.append((dl_param, r_pi))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    dl_params = [r[0] for r in results]
    ranks = [r[1] for r in results]
    
    mean_dl_param = sum(dl_params) / len(dl_params)
    mean_rank = sum(ranks) / len(ranks)
    
    covariance = sum((dl_params[i] - mean_dl_param) * (ranks[i] - mean_rank) for i in range(len(dl_params))) / len(dl_params)
    variance_dl_param = sum((dl_params[i] - mean_dl_param) ** 2 for i in range(len(dl_params))) / len(dl_params)
    variance_rank = sum((ranks[i] - mean_rank) ** 2 for i in range(len(ranks))) / len(ranks)
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_dl_param) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr_coeff > 0.7 and all(r >= 0.5 for r in ranks),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")