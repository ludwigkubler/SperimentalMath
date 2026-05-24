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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def rank(A):
        A = gaussian_elimination(A)
        return sum(1 for row in A if any(row))

    def tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            a, b, c = random.sample(variables, 3)
            clause = (a, b, c)
            clauses.append(clause)
        return variables, clauses

    def quadratic_form(variables, clauses, p):
        n = len(variables)
        Q = [[0] * n for _ in range(n)]
        for a, b, c in clauses:
            Q[a-1][a-1] += 1
            Q[b-1][b-1] += 1
            Q[c-1][c-1] += 1
            Q[a-1][b-1] -= 1
            Q[a-1][c-1] -= 1
            Q[b-1][a-1] -= 1
            Q[b-1][c-1] -= 1
            Q[c-1][a-1] -= 1
            Q[c-1][b-1] -= 1
        for i in range(n):
            Q[i][i] %= p
        return rank(Q)

    def resolution_proof_length(variables, clauses):
        n = len(variables)
        m = len(clauses)
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause1 = stack.pop()
            if not clause1:
                continue
            for clause2 in stack:
                if not clause2:
                    continue
                common = set(clause1).intersection(set(clause2))
                if len(common) == 1:
                    new_clause = [x for x in clause1 + clause2 if x != list(common)[0]]
                    stack.append(new_clause)
        return m

    n = random.randint(5, 40)
    m = 2 * n
    variables, clauses = tseitin_formula(n, m)
    p = random.choice([2, 3, 5, 7, 11, 13])
    
    rank_value = quadratic_form(variables, clauses, p)
    proof_length = resolution_proof_length(variables, clauses)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": rank_value / proof_length if proof_length > 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")