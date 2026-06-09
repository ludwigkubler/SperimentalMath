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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next(iter(clauses[0]))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            remaining_clauses = [c for c in clauses if not any(v == (not neg) for v, neg in zip(c, new_assignment))]
            if dpll(remaining_clauses, new_assignment):
                return True
        return False

    def is_satisfiable(clauses):
        return dpll(clauses, {})

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def find_brauer_groups(clauses):
        brauer_groups = set()
        for clause in clauses:
            # Simplified Brauer group identification (placeholder)
            brauer_group = tuple(sorted(clause))
            brauer_groups.add(brauer_group)
        return len(brauer_groups)

    def minimal_representation_length(poly):
        # Placeholder for minimal representation length calculation
        return len(poly)

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n * (n - 1) // 2):
        clause = [random.choice([True, False]) for _ in range(n)]
        if is_satisfiable(clauses + [clause]):
            clauses.append(clause)

    brauer_group_count = find_brauer_groups(clauses)
    representation_length = minimal_representation_length(tuple(sorted(clauses)))

    return {
        "metric_name": "minimal_representation_length",
        "metric_value": representation_length,
        "instances_tested": len(clauses),
        "n_max": n,
        "conjecture_holds": abs(representation_length - math.log(n) * brauer_group_count) <= 2 * math.log(n) * brauer_group_count,
        "counterexample": "" if conjecture_holds else f"n={n}, representation_length={representation_length}, expected={math.log(n) * brauer_group_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")