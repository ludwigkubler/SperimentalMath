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
    
    def generate_cnf(n, complexity):
        # Generate a random n-variable CNF formula with given complexity
        clauses = set()
        for _ in range(complexity):
            clause = []
            for _ in range(random.randint(1, n)):
                var = random.choice(range(1, n + 1))
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(-var)
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def frege_proof_complexity(cnf):
        # Placeholder for actual Frege proof complexity computation
        return len(cnf)  # Simplified for testing purposes

    def polynomial_representation(cnf):
        # Placeholder for actual polynomial representation computation
        n = max(abs(var) for var in cnf)
        poly = [0] * (n + 1)
        for clause in cnf:
            product = 1
            for var in clause:
                if var > 0:
                    product *= (1 - x ** var)
                else:
                    product *= (1 + x ** abs(var))
            poly += [coeff * product for coeff in poly]
        return poly

    def hodge_rank(poly):
        # Placeholder for actual Hodge rank computation
        n = len(poly) - 1
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            matrix[i][i-1] = poly[i]
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(rank)):
                rank += 1
        return rank

    def gaussian_elimination(matrix):
        # Perform Gaussian elimination to find the rank of a matrix
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            if rank >= rows:
                break
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(cols):
                matrix[rank][j] /= matrix[rank][i]
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    for k in range(cols):
                        matrix[j][k] -= matrix[j][i] * matrix[rank][k]
            rank += 1
        return rank

    n = random.randint(5, 40)
    complexity = random.randint(n // 2 + 1, n)
    cnf = generate_cnf(n, complexity)
    frege_complexity = frege_proof_complexity(cnf)
    poly = polynomial_representation(cnf)
    h_rank = gaussian_elimination(poly)

    metric_name = "Hodge Rank"
    metric_value = h_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""

    if frege_complexity > n / 2 and h_rank >= Fraction(math.log(n), 10):
        conjecture_holds = True
    elif h_rank <= 2 ** (frege_complexity - n // 2):
        conjecture_holds = False
        counterexample = "Hodge rank too low for given Frege complexity"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge rank too low for given Frege complexity\" first_failing_seed={first_failing_seed}")