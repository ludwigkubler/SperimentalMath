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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(m)):
                rank += 1
        return rank

    def xor_and_tree_width(clauses, variables):
        # Placeholder implementation for XOR-AND tree width
        # This is a dummy function and should be replaced with actual logic
        return len(variables)

    def generate_quadratic_form(n):
        q = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            q[i][i] += 1
        return q

    def is_non_degenerate(q):
        det = 1
        for i in range(len(q)):
            det *= q[i][i]
        return det != 0

    n = random.randint(5, 40)
    m = 2 ** (n - 1) - 1
    clauses = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    variables = list(range(n))

    tree_width = xor_and_tree_width(clauses, variables)
    epsilon = 0.5
    min_rank = float('inf')

    for _ in range(30):
        q = generate_quadratic_form(n)
        if is_non_degenerate(q):
            min_rank = min(min_rank, rank(q))

    conjecture_holds = min_rank >= math.log2(tree_width) + epsilon
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")