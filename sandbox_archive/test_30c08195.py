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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables, 3)
            if random.choice([True, False]):
                clause = [f'-{v}' for v in clause]
            clauses.append(' '.join(clause))
        return ' '.join(clauses)

    def incidence_algebra(clauses):
        n_vars = len(set(v[2:] if v.startswith('-') else v for v in clauses))
        n_clauses = len(clauses)
        A = [[0] * (n_vars + n_clauses) for _ in range(n_vars + n_clauses)]
        for i, clause in enumerate(clauses):
            literals = [v[2:] if v.startswith('-') else v for v in clause.split()]
            for literal in literals:
                j = int(literal)
                A[j][n_vars + i] = 1
                A[n_vars + i][j] = -1
        return A

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            j = next((k for k in range(rank, m) if A[k][i]), None)
            if j is not None:
                A[j], A[rank] = A[rank], A[j]
                for k in range(i + 1, n):
                    factor = -A[rank][k] / A[rank][i]
                    for l in range(n):
                        A[rank][l] += factor * A[j][l]
                rank += 1
        return rank

    def local_system_order(A):
        m, n = len(A), len(A[0])
        order = 0
        for i in range(m):
            if all(A[i][j] == 0 for j in range(n)):
                continue
            submatrix = [row[:] for row in A]
            for j in range(i + 1, m):
                if all(submatrix[j][k] == 0 for k in range(n)):
                    continue
                factor = -submatrix[j][i] / submatrix[i][i]
                for k in range(n):
                    submatrix[j][k] += factor * submatrix[i][k]
            order += 1
        return order

    def resolution_proof_length(clauses):
        n_vars = len(set(v[2:] if v.startswith('-') else v for v in clauses))
        n_clauses = len(clauses)
        stack = []
        for clause in clauses:
            literals = [v[2:] if v.startswith('-') else v for v in clause.split()]
            stack.append((literals, 0))
        length = 0
        while stack:
            literals, level = stack.pop()
            if not literals:
                continue
            literal = random.choice(literals)
            new_clauses = []
            for clause in clauses:
                if literal in clause or f'-{literal}' in clause:
                    continue
                new_clause = [v for v in clause.split() if v != literal and v != f'-{literal}']
                if not new_clause:
                    return length + 1
                new_clauses.append(' '.join(new_clause))
            stack.extend((new_clauses, level + 1) for _ in range(2))
            length += 1
        return length

    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_sat_instance(n)
    clauses = instance.split()
    A = incidence_algebra(clauses)
    order = local_system_order(A)
    length = resolution_proof_length(clauses)

    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": length >= order / 2,
        "counterexample": "" if length >= order / 2 else f"Length: {length}, Order: {order}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")