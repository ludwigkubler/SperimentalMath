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

def rank_of_matrix(A):
    m, n = len(A), len(A[0])
    reduced_A = gaussian_elimination(A)
    rank = sum(1 for row in reduced_A if any(row[j] != 0 for j in range(n)))
    return rank

def generate_monotone_dnf(k, n):
    variables = list(range(n))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    dnf_formula = [clauses]
    return dnf_formula

def tropicalized_lie_algebra_rank(dnf_formula):
    n = len(dnf_formula[0][0])
    A = [[0] * (2**n) for _ in range(2**n)]
    for clause in dnf_formula:
        for assignment in range(2**n):
            if all((assignment >> var) & 1 == 1 for var in clause):
                for other_assignment in range(2**n):
                    A[assignment][other_assignment] += 1
    return rank_of_matrix(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0

    for n in n_values:
        k = min(n, 10)  # Ensure k is at least 1 and at most n
        dnf_formula = generate_monotone_dnf(k, n)
        rank = tropicalized_lie_algebra_rank(dnf_formula)
        total_rank += rank
        instances_tested += 1

    metric_value = total_rank / len(n_values)
    expected_rank = sum(n**k for k in range(5, 11)) / (6 * 40)  # Average of Θ(n^k) for n=5 to n=10
    conjecture_holds = abs(metric_value - expected_rank) <= 0.3 * expected_rank
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Tropicalized Lie Algebra Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")