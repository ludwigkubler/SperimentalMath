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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
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

    def is_independent(v, basis):
        if not basis:
            return True
        for b in basis:
            if all(b[j] == v[j] for j in range(len(b))):
                return False
        return True

    def add_to_basis(v, basis):
        if is_independent(v, basis):
            basis.append(v)
        return basis

    def generate_semantic_types(n):
        types = set()
        for i in range(1 << n):
            type_ = tuple((i >> j) & 1 for j in range(n))
            types.add(type_)
        return types

    def assign_semantic_types(clauses, types):
        assignment = {}
        for clause in clauses:
            for t in types:
                if all(abs(c) == t[i] for i, c in enumerate(clause)):
                    assignment[clause] = t
                    break
        return assignment

    def calculate_width(assignment):
        basis = []
        for clause in assignment:
            v = tuple(1 if abs(c) in assignment else 0 for c in clause)
            add_to_basis(v, basis)
        return len(basis)

    n = random.randint(5, 40)
    clauses = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(n)]
    types = generate_semantic_types(n)
    assignment = assign_semantic_types(clauses, types)
    width = calculate_width(assignment)

    k_pi = len(types)
    conjecture_holds = width <= 2 ** (k_pi - 1) and k_pi <= math.log2(len(types))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "width",
        "metric_value": width,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")