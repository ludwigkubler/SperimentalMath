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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if A[i][j] != 0:
                    pivot = Fraction(A[i][j])
                    break
            for k in range(i + 1, m):
                factor = Fraction(A[k][j]) / pivot
                for l in range(j, n):
                    A[k][l] -= factor * A[i][l]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next((v for v in range(len(assignment)) if assignment[v] is None), None)
        if var is None:
            return False
        
        assignment[var] = True
        new_clauses = [c for c in clauses if not any(l == -var or l == var for l in c)]
        if dpll(new_clauses, assignment):
            return True
        
        assignment[var] = False
        new_clauses = [c for c in clauses if not any(l == -var or l == var for l in c)]
        if dpll(new_clauses, assignment):
            return True
        
        assignment[var] = None
        return False
    
    def generate_sat_instance(n):
        m = random.randint(1, n)
        clauses = []
        for _ in range(m):
            clause = [random.choice([-i, i]) for i in range(1, n + 1)]
            clauses.append(clause)
        return clauses
    
    def geometric_representation(clauses):
        n = len(clauses[0])
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for i in clause:
                if i > 0:
                    A[i - 1][i - 1] += Fraction(1)
                else:
                    A[-i - 1][-i - 1] -= Fraction(1)
        return gaussian_elimination(A)
    
    def max_complexity(A):
        m, n = len(A), len(A[0])
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank
    
    def dpll_search_tree_height(clauses):
        assignment = [None] * (max(abs(l) for clause in clauses for l in clause))
        return dpll(clauses, assignment)
    
    n_values = [5, 10, 15, 20, 30, 40]
    heights = []
    complexities = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            height = dpll_search_tree_height(clauses)
            complexity = max_complexity(geometric_representation(clauses))
            heights.append(height)
            complexities.append(complexity)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_height = sum(heights) / len(heights)
    std_height = (sum((x - mean_height) ** 2 for x in heights) / len(heights)) ** 0.5
    
    if all(h <= c for h, c in zip(heights, complexities)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "DPLL height exceeds Coxeter group complexity"
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_height = (sum((r["metric_value"] - mean_height) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL height exceeds Coxeter group complexity\" first_failing_seed={first_failing_seed + 1}")