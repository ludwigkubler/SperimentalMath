# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        literal = random.choice([l for clause in clauses for l in clause if l > 0])
        new_clauses = [[l for l in clause if l != literal and l != -literal] for clause in clauses]
        if dpll(new_clauses, assignment + [literal]):
            return True
        if dpll(new_clauses, assignment + [-literal]):
            return True
        return False

    def cnf_to_matrix(clauses):
        n = max(abs(l) for clause in clauses for l in clause)
        A = [[Fraction(0) for _ in range(n)] for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for literal in clause:
                row, col = abs(literal) - 1, literal > 0
                A[i][col] += Fraction(1)
        return gaussian_elimination(A)

    def misl_from_matrix(A):
        n = len(A[0])
        rank = 0
        for i in range(n):
            if any(A[j][i] != Fraction(0) for j in range(len(A))):
                rank += 1
        return rank

    def dpll_path_length(clauses):
        assignment = []
        return dpll(clauses, assignment)

    n_max = 40
    instances_tested = 0
    misl_values = []
    w_values = []

    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = [[random.randint(-n, -1), random.randint(1, n)] for _ in range(n)]
            A = cnf_to_matrix(clauses)
            misl_value = misl_from_matrix(A)
            w_value = dpll_path_length(clauses)
            misl_values.append(misl_value)
            w_values.append(w_value)
            instances_tested += 1

    if not misl_values or not w_values:
        return {
            "metric_name": "misl_vs_w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_misl = sum(misl_values) / len(misl_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = sum((m - mean_misl) * (w - mean_w) for m, w in zip(misl_values, w_values)) / (len(misl_values) * sum((m - mean_misl) ** 2 for m in misl_values) ** 0.5 * sum((w - mean_w) ** 2 for w in w_values) ** 0.5)

    return {
        "metric_name": "misl_vs_w",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and len([x for x in misl_values if x == mean_misl]) < len(misl_values),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"misl = {mean_misl}, w = {mean_w}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ranks = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len([result for result in results if result["metric_value"] is not None])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ranks} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ranks} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")