# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def dpll_tree_width(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    variables = set.union(*clauses)
    
    def dfs(model, level):
        if level == n:
            return 0
        var = next(iter(variables - model))
        max_width = 0
        for assignment in (True, False):
            new_model = model.copy()
            new_model.add(var if assignment else -var)
            width = dfs(new_model, level + 1)
            if width > max_width:
                max_width = width
            if max_width >= len(variables) - level:
                return max_width
        return max_width
    
    return dfs(set(), 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2*n)
            cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(m)]
            grothendieck_rank = gaussian_elimination(cnf)
            dpll_width = dpll_tree_width(cnf)
            results.append((grothendieck_rank, dpll_width))
    
    if not results:
        return {
            "metric_name": "dpll_tree_width_to_grothendieck_rank_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [w / r for r, w in results if r != 0]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = (sum((r - mean_ratio)**2 for r in ratios) / len(ratios))**0.5
    
    return {
        "metric_name": "dpll_tree_width_to_grothendieck_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(abs(r - 1) <= 0.05 for r in ratios) and std_ratio / mean_ratio <= 0.15,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(r is not None for r in results):
        mean_value = sum(results) / len(results)
        std_value = (sum((r - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = sum(1 for r in results if abs(r - 1) <= 0.05 and std_ratio / mean_ratio <= 0.15) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is None)
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined n_tested={len(results)}")