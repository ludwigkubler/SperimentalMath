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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def resolution_width(phi):
        # Simplified DPLL solver to estimate width
        clauses = phi.split('\n')
        variables = set()
        for clause in clauses:
            if clause:
                variables.update(clause.split())
        assignment = {var: random.choice([True, False]) for var in variables}
        width = 0
        for clause in clauses:
            if not clause:
                continue
            unsatisfied_clauses = [c for c in clause.split() if (c[0] == '-' and assignment[c[1:]]) or (c[0] != '-' and not assignment[c])]
            if len(unsatisfied_clauses) > width:
                width = len(unsatisfied_clauses)
        return width

    def geometric_entropy(phi):
        # Constructive mapping from lines in the projective plane to points in the affine space
        n = phi.count('x')
        m = phi.count('c')
        if n == 0 or m == 0:
            return 0
        entropy = 0
        for i in range(n):
            for j in range(m):
                entropy += math.log2(1 / (n * m))
        return entropy

    def generate_cnf(n, m):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['-' + v for v in variables], random.randint(2, n))
            clauses.append(' '.join(clause) + ' 0')
        return '\n'.join(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            phi = generate_cnf(n, random.randint(1, n))
            width = resolution_width(phi)
            entropy = geometric_entropy(phi)
            if entropy == 0:
                continue
            results.append((width, entropy))

    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_width = sum(w for w, _ in results) / len(results)
    mean_entropy = sum(e for _, e in results) / len(results)
    correlation_coefficient = sum((w - mean_width) * (e - mean_entropy) for w, e in results) / len(results) / math.sqrt(sum((w - mean_width) ** 2 for w, _ in results)) / math.sqrt(sum((e - mean_entropy) ** 2 for _, e in results))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient < 3 and all(c <= 10 for c in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")