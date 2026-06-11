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
    
    def generate_geometric_circuit(n):
        G = []
        for i in range(n):
            G.append(random.sample(range(1, n), random.randint(1, n-1)))
        return G
    
    def incidence_algebra(G):
        n = len(G)
        A_G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A_G[i][j] = sum(len(set(G[k]) & set(G[l])) for k in range(n) if k != i and k != j)
                A_G[j][i] = A_G[i][j]
        return A_G
    
    def communication_complexity_rank(A_G):
        n = len(A_G)
        rank = 0
        for i in range(n):
            row_sum = sum(A_G[i])
            if row_sum > rank:
                rank = row_sum
        return rank
    
    def min_index_p_adic_representation(A_G):
        n = len(A_G)
        total = 0
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if A_G[i][j] != 0:
                    total += A_G[i][j]
                    count += 1
        if count == 0:
            return 0
        return Fraction(total, count)
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        G = generate_geometric_circuit(n)
        A_G = incidence_algebra(G)
        r_G = communication_complexity_rank(A_G)
        i_G = min_index_p_adic_representation(A_G)
        results.append((i_G, r_G))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    i_G_values = [i for i, _ in results]
    r_G_values = [r for _, r in results]
    correlation_coefficient = pearson_correlation_coefficient(i_G_values, r_G_values)
    p_value = 2 * (1 - math.stats.t.cdf(abs(correlation_coefficient) * math.sqrt(len(results) - 2), len(results) - 2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")