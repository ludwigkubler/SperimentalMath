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
from itertools import combinations

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def galois_representation_order(phi):
    n = len(phi)
    variables = list(range(n))
    literals = set()
    for clause in phi:
        literals.update(clause)
    literal_to_index = {l: i for i, l in enumerate(literals)}
    A = [[0] * (2 ** len(literals)) for _ in range(2 ** len(literals))]
    b = [0] * (2 ** len(literals))
    for assignment in range(2 ** len(literals)):
        assignment_bits = [(assignment >> i) & 1 for i in range(len(literals))]
        A[assignment][assignment] = 1
        for clause in phi:
            if all(assignment_bits[literal_to_index[l]] == (l.startswith('¬') ^ l[1:] in clause) for l in clause):
                b[assignment] += 1
    solution = gaussian_elimination(A, b)
    return sum(abs(x) for x in solution)

def dpll_search_tree_width(phi):
    def dpll(assignment, literals):
        if not literals:
            return 0
        literal = next(iter(literals))
        positive_clauses = [c for c in phi if literal in c]
        negative_clauses = [c for c in phi if literal.startswith('¬') and literal[1:] in c]
        if not positive_clauses:
            return dpll(assignment | {literal}, literals - {literal})
        if not negative_clauses:
            return dpll(assignment | {-int(literal)}, literals - {literal})
        return max(dpll(assignment | {literal}, literals - {literal}), dpll(assignment | {-int(literal)}, literals - {literal})) + 1
    return dpll(set(), set(range(1, len(phi) + 1)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.choice(['', '¬']) + str(random.randint(1, n)) for _ in range(random.randint(2, 3))] for _ in range(n)]
    min_order = galois_representation_order(phi)
    width = dpll_search_tree_width(phi)
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_order <= 2 * width,  # Arbitrary constant k=2 for testing
        "counterexample": "" if min_order <= 2 * width else f"min_order={min_order} > 2*width={2*width}"
    }

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    if std_x == 0 or std_y == 0:
        return 0
    return cov / (std_x * std_y)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample=\"min_order > 2*width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")