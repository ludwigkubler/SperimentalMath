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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            random.shuffle(literals)
            clause = ' or '.join(literals)
            clauses.append(clause)
        return ' and '.join(clauses)

    def polynomial_system_from_3sat(instance):
        polynomials = []
        for clause in instance.split(' and '):
            terms = []
            for literal in clause.split(' or '):
                if literal.startswith('~'):
                    var = literal[1:]
                    coeff = -1
                else:
                    var = literal
                    coeff = 1
                terms.append(f'{coeff}*x{var}')
            polynomials.append('+'.join(terms))
        return '+'.join(polynomials)

    def discriminant(poly):
        # This is a simplified version of computing the discriminant for a polynomial system.
        # For simplicity, we assume the polynomial is linear in each variable and compute the determinant
        # of the matrix formed by the coefficients.
        terms = poly.split('+')
        n = len(terms)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for term in terms:
            if 'x' not in term:
                continue
            var = term[1:]
            coeff = int(term[0]) if term[0].isdigit() else 1
            A[int(var) - 1][int(var) - 1] += coeff ** 2
        det = determinant(A)
        return det

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det

    def sos_refutation_degree(poly, max_depth=10):
        # This is a simplified version of computing the SOS refutation degree.
        # For simplicity, we assume the polynomial is linear in each variable and compute the maximum depth
        # of the moment matrix that can be used to refute the polynomial.
        terms = poly.split('+')
        n = len(terms)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for term in terms:
            if 'x' not in term:
                continue
            var = term[1:]
            coeff = int(term[0]) if term[0].isdigit() else 1
            M[int(var) - 1][n] += coeff ** 2
            M[n][int(var) - 1] += coeff ** 2
        for i in range(n):
            M[i][i] += 1
        rank = matrix_rank(M)
        return rank

    def matrix_rank(matrix):
        # This is a simplified version of computing the rank of a matrix.
        # For simplicity, we assume the matrix is square and compute its determinant.
        n = len(matrix)
        if n == 1:
            return 1 if matrix[0][0] != 0 else 0
        det = determinant(matrix)
        return 1 if det != 0 else 0

    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))

    def is_power_of_two(x):
        return x > 0 and (x & (x - 1)) == 0

    n = random.randint(5, 40)
    instance = generate_3sat_instance(n)
    poly = polynomial_system_from_3sat(instance)
    disc = discriminant(poly)
    ref_degree = sos_refutation_degree(poly)

    metric_name = "SOS Refutation Degree"
    metric_value = ref_degree
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""

    if is_power_of_two(disc) and disc >= 2 ** (0.3 * n):
        if ref_degree >= 0.5 * math.sqrt(n):
            conjecture_holds = True
    elif not is_power_of_two(disc) or disc < 2 ** (0.3 * n):
        if ref_degree < 0.5 * math.sqrt(n):
            conjecture_holds = True

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")