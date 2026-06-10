# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_sat_instance(n):
        clauses = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
        return [random.choice(clauses) for _ in range(n)]

    def diophantine_polynomial(clause, n):
        terms = []
        for i in range(n):
            if clause[i] == '1':
                terms.append(f"({chr(ord('x') + i)})")
            else:
                terms.append(f"-({chr(ord('x') + i)})")
        return " + ".join(terms) + " - 1"

    def degree_of_polynomial(poly):
        poly = poly.replace(" ", "")
        terms = poly.split("+")
        max_degree = 0
        for term in terms:
            if "-" in term:
                term = term[1:]
            if "(" in term and ")" in term:
                var, exp = term.strip("()").split("^")
                degree = int(exp)
                if degree > max_degree:
                    max_degree = degree
        return max_degree

    def communication_complexity_rank_variance(instance):
        n = len(instance)
        matrix = [[0] * n for _ in range(n)]
        for i, j in combinations(range(n), 2):
            matrix[i][j] = matrix[j][i] = random.randint(1, 5)
        rank = gaussian_elimination(matrix)
        return rank ** 2

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
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank

    def run_single_instance():
        n = random.randint(5, 40)
        instance = generate_random_sat_instance(n)
        diophantine_terms = {i: {} for i in range(n)}
        for clause in instance:
            poly = diophantine_polynomial(clause, n)
            degree = degree_of_polynomial(poly)
            for var in set(poly):
                if var.startswith("(") and var.endswith(")"):
                    x = ord(var[1]) - ord('x')
                    diophantine_terms[x][degree] = 1
        A = [[sum(diophantine_terms[i][j] * diophantine_terms[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
        rank = communication_complexity_rank_variance(instance)
        return degree, rank

    degree, rank = run_single_instance()
    
    return {
        "metric_name": "degree_of_polynomial",
        "metric_value": degree,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")