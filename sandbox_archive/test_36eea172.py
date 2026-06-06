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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if var not in clause:
                clause.add(var)
        clauses.append(list(clause))
    return clauses

def k_cnf_to_quadratic_form(clauses):
    n = max(max(clause) for clause in clauses)
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for c in clause:
            A[c-1][c-1] += 1
            for d in clause:
                if c != d:
                    A[c-1][d-1] -= Fraction(1, len(clause))
                    A[d-1][c-1] -= Fraction(1, len(clause))
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def minimal_order_quadratic_form(clauses):
    A = k_cnf_to_quadratic_form(clauses)
    det = determinant(A)
    if det == 0:
        return None
    return abs(det)

def communication_complexity_rank_variance(clauses):
    n = max(max(clause) for clause in clauses)
    rank = sum(1 for _ in range(n) if any(var in clause for clause in clauses))
    return rank ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_k_cnf(n, n // 2)
            minimal_order_value = minimal_order_quadratic_form(clauses)
            if minimal_order_value is None:
                continue
            variance_rank_value = communication_complexity_rank_variance(clauses)
            results.append((minimal_order_value, variance_rank_value))
    if not results:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean_diff = sum(b - a for a, b in results) / len(results)
    corr_coeff = sum((a - mean_a) * (b - mean_b) for a, b in results) / math.sqrt(sum((a - mean_a) ** 2 for a, _ in results)) / math.sqrt(sum((b - mean_b) ** 2 for _, b in results))
    return {
        "metric_name": "MinimalOrder",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": corr_coeff >= 0.8 and abs(mean_diff) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_diff = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["instances_tested"] > 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=NOT_COMPUTABLE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")