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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def tseitin_formula(G):
        n = len(G)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            if G[i]:
                clauses.append([literals[i]])
            else:
                clauses.append([-literals[i]])
        return clauses
    
    def resolution_refutation_length(clauses):
        stack = []
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(-x in clauses[i] and x in clauses[j] for x in set(clauses[i]) & set(clauses[j])):
                        resolvent = [x for x in clauses[i] if x not in clauses[j]] + [x for x in clauses[j] if -x not in clauses[i]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def local_index(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j] = -1
                    A[j][i] = 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def is_expander(G):
        n = len(G)
        degree_sum = sum(sum(row) for row in G)
        avg_degree = degree_sum / n
        max_degree = max(max(row) for row in G)
        return 2 * avg_degree > max_degree
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    
    ν_G = local_index(G)
    F_G = tseitin_formula(G)
    refutation_length = resolution_refutation_length(F_G)
    
    conjecture_holds = True
    counterexample = ""
    
    if ν_G > 1 and refutation_length < 2 ** ν_G:
        conjecture_holds = False
        counterexample = f"ν(G)={ν_G}, refutation_length={refutation_length}"
    elif ν_G == 1 and refutation_length > 2:
        conjecture_holds = False
        counterexample = f"ν(G)={ν_G}, refutation_length={refutation_length}"
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and not any(r["counterexample"] == "mapping_undefined" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")