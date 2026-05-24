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
    
    n = random.choice([10, 20, 40])
    k = random.randint(3, 5)
    F = []
    for _ in range(n):
        clause = [random.randint(-n, n) for _ in range(k)]
        if all(abs(x) > 0 for x in clause):
            F.append(clause)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = A[j][i] / A[rank][i]
                    for l in range(n):
                        A[j][l] -= factor * A[rank][l]
            rank += 1
        return rank
    
    def local_defect_complexity(F):
        m, n = len(F), len(F[0])
        A = [[0] * (n + m) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                A[i][j] = F[i][j]
            A[i][n + i] = 1
        return gaussian_elimination(A)
    
    def dpll_refutation_path_length(F):
        # Simplified DPLL solver to estimate path length
        stack = []
        assignment = [0] * (max(abs(x) for clause in F for x in clause) + 1)
        def solve():
            if not F:
                return 1
            var = next((x for x in range(1, len(assignment)) if all(x not in clause or assignment[abs(x)] == -sign for clause, sign in zip(F, [1] * len(F)))), None)
            if var is None:
                return 0
            assignment[var] = 1
            F_pos = [clause for clause in F if var not in clause]
            assignment[-var] = 1
            F_neg = [clause for clause in F if -var not in clause]
            return solve() + solve()
        return solve()
    
    L_F = local_defect_complexity(F)
    t_star_F = dpll_refutation_path_length(F)
    alpha = 2  # Simplified constant for this example
    ratio = t_star_F / (alpha * L_F)
    
    conjecture_holds = ratio <= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 1.5"
    
    return {
        "metric_name": "DPLL Path Length vs Local Defect Complexity",
        "metric_value": ratio,
        "instances_tested": len(F),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std={math.sqrt(sum((r['metric_value'] - mean_ratio)**2 for r in results) / len(results)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")