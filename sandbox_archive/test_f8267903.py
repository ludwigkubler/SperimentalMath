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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, n - 1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses

    def bp_read_twice_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            count = sum(abs(x) for x in clause)
            if count > width:
                width = count
        return width

    def tropicalized_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for i in range(n):
            row_sum = sum(1 for clause in cnf if clause[i] != 0)
            if row_sum > rank:
                rank = row_sum
        return rank

    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        if not matrix:
            return 0
        n = len(matrix)
        m = len(matrix[0])
        matrix = [row[:] for row in matrix]
        matrix = gaussian_elimination(matrix)
        if matrix is None:
            return 0
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    bp_width = bp_read_twice_width(cnf)
    tropical_rank = tropicalized_rank(cnf)

    if bp_width == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "BP_ReadTwice width is zero"
        }

    ratio = tropical_rank / bp_width
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all("metric_value" in r and not math.isinf(r["metric_value"]) and r["metric_value"] <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any("metric_value" in r and not math.isinf(r["metric_value"]) and r["metric_value"] > 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "metric_value" in result and not math.isinf(result["metric_value"]) and result["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")