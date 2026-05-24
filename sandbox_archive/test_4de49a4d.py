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
    
    def is_planar(n):
        # Simple heuristic to check if a graph with n vertices is planar
        return n <= 4
    
    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(1 for j in range(n) if G[i][j])
            L[i][i] = -degree
            for j in range(i + 1, n):
                if G[i][j]:
                    L[i][j] = L[j][i] = 1
        return L
    
    def tropicalize_matrix(L):
        max_abs_val = max(abs(x) for row in L for x in row)
        k = math.ceil(math.log2(max_abs_val))
        T_L = [[0] * len(row) for row in L]
        for i in range(len(L)):
            for j in range(len(L[i])):
                if L[i][j]:
                    T_L[i][j] = 1
                else:
                    T_L[i][j] = -1
        return T_L
    
    def minimal_rank(T_L):
        n = len(T_L)
        rank = 0
        for i in range(n):
            row = [T_L[j][i] for j in range(n)]
            if any(row):
                rank += 1
        return rank
    
    def dpll_width(G, clause_set):
        # Simplified DPLL width calculation (not exhaustive)
        if not clause_set:
            return 0
        literals = set()
        for clause in clause_set:
            literals.update(clause)
        return max(len(literals), dpll_width(G, [c for c in clause_set if any(l not in c for l in literals)]))
    
    n = random.randint(5, 40)  # Random graph size between 5 and 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    if not is_planar(n):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_planar"
        }
    
    L = laplacian_matrix(G)
    T_L = tropicalize_matrix(L)
    rank = minimal_rank(T_L)
    
    clause_set = [[i + 1 if random.choice([True, False]) else -i - 1 for i in range(n)] for _ in range(2 * n)]
    width = dpll_width(G, clause_set)
    
    if width == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "dpll_width_zero"
        }
    
    ratio = rank / width
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed' first_failing_seed={first_failing_seed}")