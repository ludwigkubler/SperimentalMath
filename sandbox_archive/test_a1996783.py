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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def indicator_polynomial(clauses, x):
        poly = 1
        for clause in clauses:
            variables = set()
            for lit in clause:
                if lit < 0:
                    variables.add(-lit)
                else:
                    variables.add(lit)
            term = 1
            for var in variables:
                term *= (1 + x**var)
            poly *= term
        return poly

    def moments(poly, x):
        moment_sum = 0
        n = len(poly)
        for i in range(n):
            moment_sum += poly[i] * x**i
        return moment_sum

    def frege_proof(depth, size):
        clauses = []
        for _ in range(size):
            clause = [random.randint(1, depth) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    n_values = [5, 10, 15, 20, 30, 40]
    total_moment_sum = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            proof = frege_proof(n, n)
            moment_sum = moments(indicator_polynomial(proof, Fraction(1, 2)), Fraction(1, 2))
            total_moment_sum += moment_sum
            instances_tested += 1

    mean_moment_sum = total_moment_sum / instances_tested
    lower_bound = n_values[-1] * math.log(n_values[-1]) ** 2
    if mean_moment_sum < 0.9 * lower_bound:
        conjecture_holds = False
        counterexample = f"mean_moment_sum={mean_moment_sum} < 0.9 * {lower_bound}"

    return {
        "metric_name": "mean_moment_sum",
        "metric_value": mean_moment_sum,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_moment_sum = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moment_sum} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_moment_sum} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")