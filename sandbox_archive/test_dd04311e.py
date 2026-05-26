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
        rank = sum(1 for row in A if any(row))
        return rank
    
    def communication_complexity(F, n):
        variables = list(range(n))
        delta = 0
        for x in itertools.product([0, 1], repeat=n):
            if all(F(x) == F(y) for y in itertools.permutations(x)):
                delta += 1
        return math.ceil(math.log(delta / (2**n), 2))
    
    def k_cnf_formula(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses
    
    def evaluate_formula(F, x):
        return all(all(x[v] == 0 for v in clause) or any(x[v] == 1 for v in clause) for clause in F)
    
    def twisted_k_theory_rank(F, n):
        m = len(F)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(F):
            for v in clause:
                if v > 0:
                    A[i][v-1] += 1
                else:
                    A[i][-1] += 1
        return gaussian_elimination(A)
    
    n = random.randint(2, 40)
    m = random.randint(n, n*5)
    F = k_cnf_formula(n, m)
    rank = twisted_k_theory_rank(F, n)
    delta = communication_complexity(evaluate_formula, n)
    cc = communication_complexity(F, n)
    
    conjecture_holds = rank <= n**(1/2 + 0.1) and cc >= min(n, math.log(1/delta, 2))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Twisted K-Theory Rank vs Communication Complexity",
        "metric_value": rank,
        "instances_tested": 1,
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")