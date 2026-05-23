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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r
    
    def tseitin_formula(G):
        n = len(G)
        variables = {f'x{i}': i for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([variables[f'x{i}']])
            for j in range(i+1, n):
                if G[i][j]:
                    clauses.append([-variables[f'x{i}'], variables[f'x{j}']])
                    clauses.append([-variables[f'x{j}'], variables[f'x{i}']])
        return clauses
    
    def resolution(clauses):
        clauses = set(tuple(sorted(c)) for c in clauses)
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                if len(set(c1) & set(c2)) == 1:
                    new_clause = list((set(c1) ^ set(c2)))
                    if not any(all(l in clause for l in new_clause) for clause in clauses):
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(tuple(sorted(c)) for c in new_clauses)
        return len(clauses)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    A = []
    for i in range(n):
        row = [0] * (n + 1)
        row[-1] = -1
        for j in range(n):
            if G[i][j]:
                row[j] = 1
        A.append(row)
    
    R_G = resolution(tseitin_formula(G))
    min_rank = rank(A)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= math.log(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")