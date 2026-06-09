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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        literals_seen = set()
        while queue:
            clause1 = queue.pop(0)
            if not clause1:
                continue
            literal_to_remove = None
            for lit in clause1:
                if -lit in literals_seen:
                    literal_to_remove = lit
                    break
            if literal_to_remove is None:
                return len(queue) + 1
            literals_seen.add(literal_to_remove)
            new_clauses = []
            for clause2 in queue:
                if literal_to_remove in clause2:
                    new_clause = [x for x in clause2 if x != literal_to_remove and -x not in clause1]
                    if new_clause:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return len(queue)

    def vector_space_dimension(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit - 1] += 1
                else:
                    matrix[-1][abs(lit) - 1] += 1
        rank = gaussian_elimination(matrix)
        return n - rank

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j == i:
                    continue
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    dimensions = []

    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        dimension = vector_space_dimension(cnf)
        widths.append(width)
        dimensions.append(dimension)

    correlation_coefficient = calculate_correlation_coefficient(dimensions, widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def calculate_correlation_coefficient(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.7' first_failing_seed={first_failing_seed}")