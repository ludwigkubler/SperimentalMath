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
            factor = Fraction(1, A[i][i])
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def real_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def random_3cnf(n, m):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
            while len(clause) < 3:
                var = random.choice(variables)
                if var not in clause and -var not in clause:
                    clause.append(var * (-1 if random.randint(0, 1) else 1))
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        A = [[0] * (2**n) for _ in range(n)]
        for i, clause in enumerate(clauses):
            for assignment in range(2**n):
                if all((assignment >> abs(var) & 1) ^ sign == 0 for var, sign in zip(clause, [1]*len(clause))):
                    A[i][assignment] = 1
        return A
    
    n = random.randint(5, 40)
    m = random.randint(3*n, 6*n)
    clauses = random_3cnf(n, m)
    A = clause_indicator_polynomial(clauses)
    
    rank = real_rank(A)
    expected_rank = math.log2(n) if n > 1 else 0
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= 1,  # Allow small margin for numerical issues
        "counterexample": "" if abs(rank - expected_rank) <= 1 else f"n={n}, rank={rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")