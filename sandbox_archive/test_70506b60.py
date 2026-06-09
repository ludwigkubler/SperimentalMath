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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 2 * n
    variables = set(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)

    def dpll(phi, assignment):
        if not phi:
            return True
        literal = next(lit for lit in phi[0] if lit > 0 and lit not in assignment)
        if literal is None:
            return False
        assignment[literal] = True
        new_phi = [c for c in phi if literal not in c and -literal not in c]
        if dpll(new_phi, assignment):
            return True
        del assignment[literal]
        assignment[-literal] = True
        new_phi = [c for c in phi if -literal not in c and literal not in c]
        if dpll(new_phi, assignment):
            return True
        del assignment[-literal]
        return False

    def resolution(phi):
        clauses = list(phi)
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    c1, c2 = clauses[i], clauses[j]
                    if any(-lit in c1 and lit in c2 for lit in variables):
                        new_clause = [l for l in c1 if l not in [-lit for lit in c2] for l in c2 if l not in [-lit for lit in c1]]
                        if len(new_clause) == 0:
                            return True
                        new_clauses.append(new_clause)
            if all(clause in clauses for clause in new_clauses):
                break
            clauses.extend(new_clauses)
        return False

    phi = set(tuple(c) for c in clauses)
    proof_width = resolution(phi)

    quiver_edges = []
    for clause in clauses:
        for literal in clause:
            if literal > 0:
                quiver_edges.append((literal, -literal))
            else:
                quiver_edges.append((-literal, literal))

    A = [[0.0] * (2 * n) for _ in range(2 * n)]
    b = [0.0] * (2 * n)
    for i in range(2 * n):
        if i < n:
            A[i][i] = 1.0
        else:
            A[i][n + i - n] = 1.0

    x = gaussian_elimination(A, b)

    representation_length = sum(abs(x[i]) for i in range(2 * n))

    return {
        "metric_name": "representation_length",
        "metric_value": representation_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": proof_width >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")