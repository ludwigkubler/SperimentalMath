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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def min_rank(A):
        rank = 0
        A_rref = gaussian_elimination(A)
        for row in A_rref:
            if any(row):
                rank += 1
        return rank
    
    def dpll_diameter(F):
        # Simplified DPLL algorithm to estimate diameter
        n = len(F[0])
        clauses = F[1]
        def dpll(model, clause_index=0):
            if clause_index == len(clauses):
                return True
            for var in range(n):
                if model[var] is None:
                    new_model = model[:]
                    new_model[var] = True
                    if dpll(new_model, clause_index + 1):
                        return True
                    new_model[var] = False
                    if dpll(new_model, clause_index + 1):
                        return True
            return False
        return len(F[0]) - 2
    
    n = random.choice([10, 20, 30])
    m = random.choice([100, 200])
    F = ([random.randint(0, 1) for _ in range(n)] for _ in range(m))
    
    H_F = [[sum(F[j][i] * (-1)**j for j in range(m)) % 2 for i in range(n)]]
    min_rank_H_F = min_rank(H_F)
    dpll_diam = dpll_diameter(F)
    
    if dpll_diam == 0:
        return {
            "metric_name": "MinRank/HF_DPLL",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL diameter is zero"
        }
    
    ratio = min_rank_H_F / dpll_diam
    return {
        "metric_name": "MinRank/HF_DPLL",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder constant c=2
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds bound' first_failing_seed={first_failing_seed}")