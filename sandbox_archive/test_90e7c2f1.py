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
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1)**i * A[0][i] * determinant(submatrix)
        return det

    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
        return variables, clauses

    def min_local_system_rank(clauses):
        m = len(clauses)
        A = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                if any(lit in clauses[i] and -lit in clauses[j] for lit in variables):
                    A[i][j] = 1
                    A[j][i] = 1
        return determinant(gaussian_elimination(A))

    def resolution_width(clauses):
        queue = clauses[:]
        resolvents = set()
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                return len(resolvents)
            for lit in clause:
                if -lit in resolvents:
                    continue
                new_clause = [l for l in clause if l != lit]
                for other_clause in queue + list(resolvents):
                    if any(lit2 in other_clause and -lit2 in new_clause for lit2 in variables):
                        new_resolvent = sorted([l for l in new_clause + other_clause if l > 0])
                        if new_resolvent not in resolvents:
                            resolvents.add(new_resolvent)
                            queue.append(new_resolvent)
        return len(resolvents)

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        m_lr = min_local_system_rank(clauses)
        w = resolution_width(clauses)
        metrics.append((m_lr, w))

    if not metrics:
        return {
            "metric_name": "min_local_system_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    m_lr_avg = sum(m for m, w in metrics) / len(metrics)
    w_avg = sum(w for m, w in metrics) / len(metrics)
    if abs(m_lr_avg - w_avg) > 2 * n_values[0]:
        return {
            "metric_name": "min_local_system_rank",
            "metric_value": m_lr_avg,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"m_lr = {m_lr_avg}, w = {w_avg}"
        }

    return {
        "metric_name": "min_local_system_rank",
        "metric_value": m_lr_avg,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_lr and w are not linearly correlated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")