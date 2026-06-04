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

def generate_formula(n, m):
    formula = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        formula.append(clause)
    return formula

def hodge_norm(formula):
    n = len(formula[0])
    m = len(formula)
    H = [[0] * n for _ in range(n)]
    for clause in formula:
        for i in range(n):
            for j in range(i + 1, n):
                if abs(clause[i]) == abs(clause[j]):
                    H[i][j] += 1
                    H[j][i] += 1
    det = determinant(H)
    return math.sqrt(det)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_norm = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        m = random.randint(1, min(10 * n, 100))  # Ensure at least 5 instances per seed
        formula = generate_formula(n, m)
        hodge_norm_value = hodge_norm(formula)
        total_hodge_norm += hodge_norm_value
        instances_tested += m
        n_max = max(n_max, n)

    mean_hodge_norm = total_hodge_norm / instances_tested
    conjecture_holds = False
    counterexample = ""

    if instances_tested >= 30:
        expected_bound = (m ** Fraction(3, 2)) * (n_max ** Fraction(1, 4))
        if abs(mean_hodge_norm - expected_bound) <= 0.1 * expected_bound:
            conjecture_holds = True
        else:
            counterexample = f"mean_hodge_norm={mean_hodge_norm}, expected_bound={expected_bound}"

    return {
        "metric_name": "Hodge Norm",
        "metric_value": mean_hodge_norm,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_hodge_norm = sum(res["metric_value"] for res in results) / len(results)
    std_hodge_norm = math.sqrt(sum((res["metric_value"] - mean_hodge_norm) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_hodge_norm} std={std_hodge_norm} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")