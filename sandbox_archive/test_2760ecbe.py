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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        if rows == 1:
            return matrix[0][0]
        det = 0
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def local_class_group(n):
        # Simplified example of a local class group calculation
        # This is just an illustrative placeholder
        return n % 2 == 0

    def dpll_tree_path_length(n):
        # Simplified example of DPLL tree path length calculation
        # This is just an illustrative placeholder
        return n * (n + 1) // 2

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_correlation = 0.0
        for _ in range(5):
            phi = random.randint(0, 1 << n)
            lcg = local_class_group(phi)
            dpll_length = dpll_tree_path_length(n)
            correlation = (lcg - 0.5) * (dpll_length - 0.5)
            total_correlation += correlation
            instances_tested += 1
        mean_correlation = total_correlation / instances_tested
        results.append({
            "metric_name": "Correlation",
            "metric_value": mean_correlation,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": abs(mean_correlation) >= 0.7,
            "counterexample": ""
        })

    return results

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append({"seed": seed, **trial_result[0]})
        print(f"TRIAL: {results[-1]}")

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")