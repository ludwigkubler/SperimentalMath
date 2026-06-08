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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
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
            clauses.append((i,))
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return variables, clauses

    def resolution_width(clauses):
        queue = list(clauses)
        seen = set()
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                return len(queue)
            for literal in clause:
                if -literal in seen:
                    continue
                seen.add(literal)
                new_clause = []
                for other_clause in queue:
                    if literal in other_clause:
                        new_clause.extend([l for l in other_clause if l != literal])
                    elif -literal in other_clause:
                        new_clause.extend([l for l in other_clause if l != -literal])
                if not new_clause:
                    return len(queue)
                queue.append(new_clause)
        return len(queue)

    def minimal_representation_degree(n):
        variables, clauses = tseitin_formula(n)
        field_size = 2**n
        A = [[0 for _ in range(field_size)] for _ in range(field_size)]
        for i in range(1, field_size):
            for j in range(1, field_size):
                if (i & j) == 0:
                    A[i][j] = 1
        rank = gaussian_elimination(A)
        return len(rank)

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        variables, clauses = tseitin_formula(n)
        width = resolution_width(clauses)
        degree = minimal_representation_degree(n)
        if width == 0:
            continue
        log_width = math.log(width)
        metric_values.append((log_width, degree))
    
    correlation_coefficient = sum(x * y for x, y in metric_values) / (sum(x**2 for x, _ in metric_values) * sum(y**2 for _, y in metric_values)) ** 0.5
    conjecture_holds = -0.5 <= correlation_coefficient <= 0.5
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")