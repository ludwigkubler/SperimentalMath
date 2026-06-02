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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(cols):
                matrix[i][j] /= pivot
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(cols)))
        return rank

    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            stack.append(literal)
            clauses = [c for c in clauses if literal not in c and -literal not in c]
        return len(stack)

    def generate_cnf(num_vars, num_clauses):
        cnf = []
        literals = list(range(1, num_vars + 1)) + [-i for i in range(1, num_vars + 1)]
        for _ in range(num_clauses):
            clause = random.sample(literals, random.randint(2, 3))
            cnf.append(clause)
        return cnf

    n_max = 40
    instances_tested = 0
    total_rank = 0
    total_width = 0
    min_rank = float('inf')
    max_rank = float('-inf')

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, n)
            rank_value = rank(cnf)
            width_value = resolution_width(cnf)
            total_rank += rank_value
            total_width += width_value
            instances_tested += 1
            min_rank = min(min_rank, rank_value)
            max_rank = max(max_rank, rank_value)

    if n_max < 16:
        return {
            "metric_name": "rank_vs_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }

    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(r * w for r, w in zip(range(min_rank, max_rank + 1), range(min_rank, max_rank + 1))) -
                               instances_tested * mean_rank * mean_width) / \
                              math.sqrt((instances_tested * sum(r**2 for r in range(min_rank, max_rank + 1)) - instances_tested * mean_rank**2) *
                                        (instances_tested * sum(w**2 for w in range(min_rank, max_rank + 1)) - instances_tested * mean_width**2))

    return {
        "metric_name": "rank_vs_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")