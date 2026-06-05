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
    
    def generate_cnf(n):
        return [[random.choice([1, -1]) * (i + 1) for i in range(n)] for _ in range(n)]
    
    def dpll(cnf):
        if not cnf:
            return True
        clause = next((c for c in cnf if any(x > 0 for x in c)), [])
        if not clause:
            return False
        p = abs(clause[0])
        if any(dpll([c for c in cnf if all(x != p or x == -y for y in c)]) for x in [p, -p]):
            return True
        return False
    
    def geometric_flow_order(cnf):
        n = len(cnf)
        distance_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                distance_matrix[i][j] = distance_matrix[j][i] = sum(abs(x - y) for x, y in zip(cnf[i], cnf[j]))
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i + 1, n):
                    factor = A[j][i] / A[i][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
            return A
        
        reduced_matrix = gaussian_elimination(distance_matrix)
        rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    dpll_depth = len(dpll(cnf)) - 1
    flow_order = geometric_flow_order(cnf)
    
    return {
        "metric_name": "Ratio of Flow Order to DPLL Depth",
        "metric_value": Fraction(flow_order, dpll_depth) if dpll_depth > 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": flow_order == dpll_depth,
        "counterexample": "" if flow_order == dpll_depth else f"Flow Order: {flow_order}, DPLL Depth: {dpll_depth}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")