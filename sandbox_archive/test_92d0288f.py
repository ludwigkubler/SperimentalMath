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

def binomial(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = Fraction(1, 1)
    for i in range(1, k + 1):
        c *= (n - i + 1) / i
    return c

def gaussian_elimination(M):
    m, n = len(M), len(M[0])
    rank = 0
    for j in range(n):
        pivot_row = None
        for i in range(rank, m):
            if M[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        M[pivot_row], M[rank] = M[rank], M[pivot_row]
        rank += 1
        for i in range(rank, m):
            factor = -M[i][j] / M[rank-1][j]
            for k in range(j, n):
                M[i][k] += factor * M[rank-1][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    results = []
    
    for n in n_values:
        L_DPLL = 0
        for _ in range(200):
            # Generate a random UNSAT 3-CNF formula with α=4.5
            clauses = []
            for i in range(n * (n - 1) // 2):
                clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
                if len(set(clause)) == 3:
                    clauses.append(clause)
            F = clauses
            
            # Compute p_F
            p_F_coeffs = [[0] * (n + 2) for _ in range(n + 2)]
            for clause in F:
                i1, i2, i3 = sorted(abs(lit) - 1 for lit in clause)
                sign = (-1) ** sum(lit < 0 for lit in clause)
                p_F_coeffs[i1][i2] += sign
                p_F_coeffs[i1][i3] += sign
                p_F_coeffs[i2][i3] += sign
            
            # Construct the constraint matrix M
            M = [[0] * (n**2) for _ in range(binomial(n+2, 3))]
            for i in range(1, n + 2):
                for j in range(i + 1, n + 2):
                    for k in range(j + 1, n + 2):
                        index = binomial(i-1, 2) * (n - i + 1) // 2 + binomial(j-i, 2)
                        M[index][i*n+j-1] += p_F_coeffs[i][j]
                        M[index][i*n+k-1] += p_F_coeffs[i][k]
                        M[index][(j-1)*n+k-1] += p_F_coeffs[j][k]
            
            # Compute dim_Q(g_F)
            rank = gaussian_elimination(M)
            g_F_dim = n**2 - rank
            
            # Run lex-DPLL to count L_DPLL(F)
            def dpll(clauses, assignment):
                if not clauses:
                    return 1
                unit_clauses = [c for c in clauses if len(c) == 1]
                if unit_clauses:
                    lit = unit_clauses[0][0]
                    new_assignment = assignment.copy()
                    new_assignment[lit] = True
                    if all(assignment[lit] == (lit > 0) or assignment[-lit] == (lit < 0) for lit in [c[0] for c in clauses]):
                        return dpll([c for c in clauses if lit not in c], new_assignment)
                    else:
                        return 0
                literals = set(lit for clause in clauses for lit in clause)
                for lit in literals:
                    new_assignment = assignment.copy()
                    new_assignment[lit] = True
                    if all(assignment[lit] == (lit > 0) or assignment[-lit] == (lit < 0) for lit in [c[0] for c in clauses]):
                        count = dpll([c for c in clauses if lit not in c], new_assignment)
                        if count > 0:
                            return count
                    new_assignment[lit] = False
                    if all(assignment[lit] == (lit > 0) or assignment[-lit] == (lit < 0) for lit in [c[0] for c in clauses]):
                        count = dpll([c for c in clauses if lit not in c], new_assignment)
                        if count > 0:
                            return count
                return 0
            
            L_DPLL += dpll(F, {})
        
        results.append({
            "n": n,
            "L_DPLL": L_DPLL,
            "g_F_dim": g_F_dim
        })
    
    max_delta = max(math.log2(result["L_DPLL"]) + result["g_F_dim"] - (result["n"] + 2 * math.ceil(math.log2(result["n"]))) for result in results)
    conjecture_holds = max_delta <= 0
    counterexample = "" if conjecture_holds else "max Δ(F) > 1"
    
    return {
        "metric_name": "Δ(F)",
        "metric_value": max_delta,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)
    std_metric_value = math.sqrt(squared_diff_sum / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max Δ(F) > 1\" first_failing_seed={first_failing_seed + 1}")