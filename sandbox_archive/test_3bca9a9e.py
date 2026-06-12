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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

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
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                det += ((-1) ** j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det

    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if any(A[i]):
                r += 1
        return r

    def random_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        # Simplified resolution width calculation
        return len(cnf)

    def tropical_modular_form(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    A[lit][lit] += 1
                    b[lit] += 1
                else:
                    A[-lit][-lit] += 1
                    b[-lit] -= 1
        return rank(gaussian_elimination(A, b))

    n_max = 40
    instances_tested = 30
    mrank_values = []
    width_values = []

    for _ in range(instances_tested):
        n = random.randint(5, min(n_max, 20))
        m = random.randint(10, 2 * n)
        cnf = random_cnf(n, m)
        mrank = tropical_modular_form(cnf)
        width = resolution_width(cnf)
        mrank_values.append(mrank)
        width_values.append(width)

    correlation_coefficient = sum((mrank_values[i] - mean_mrank) * (width_values[i] - mean_width) for i in range(instances_tested)) / instances_tested
    mean_mrank = sum(mrank_values) / instances_tested
    mean_width = sum(width_values) / instances_tested

    conjecture_holds = correlation_coefficient >= 0.8 and all(mrank <= 3 * width for mrank, width in zip(mrank_values, width_values))
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 or r["mrank"] > 3 * r["width"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")