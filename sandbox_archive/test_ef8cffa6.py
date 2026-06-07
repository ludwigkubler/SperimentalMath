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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def incidence_algebra(cnf):
        n = max(abs(lit) for lit in set([x for clause in cnf for x in clause]))
        algebra = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j and abs(i) == abs(j):
                        algebra[abs(i)][abs(j)] += 1
        return algebra
    
    def deligne_lusztig_tree_depth(algebra):
        n = len(algebra)
        tree_depth = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(1, i):
                if algebra[i][j] > 0:
                    tree_depth[i] = max(tree_depth[i], tree_depth[j] + 1)
        return max(tree_depth)
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf)
        rank_variances = []
        for _ in range(30):  # Sample 30 random assignments
            assignment = [random.choice([-1, 1]) for _ in range(n)]
            rank = sum(1 for clause in cnf if any(lit * assignment[abs(lit) - 1] > 0 for lit in clause))
            rank_variances.append(rank)
        return math.variance(rank_variances)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_max = 40
    instances_tested = 0
    correlation_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            algebra = incidence_algebra(cnf)
            depth = deligne_lusztig_tree_depth(algebra)
            variance = communication_complexity_rank_variance(cnf)
            correlation_values.append(pearson_correlation([depth], [variance]))
            instances_tested += 1
    
    mean_value = sum(correlation_values) / len(correlation_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in correlation_values) / len(correlation_values))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_value > 0.95,
        "counterexample": "" if mean_value > 0.95 else "mean_correlation_coefficient_below_0.95"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_correlation_coefficient_below_0.95' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")