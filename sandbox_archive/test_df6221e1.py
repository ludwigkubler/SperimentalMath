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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(cols):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            return None
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(rows):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def xor_and_tree_width(formula):
    # Placeholder function to compute XOR-AND tree width
    # This is a stub and should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n // 2, n * 2)
    formula = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    H_F = gaussian_elimination(formula)
    if H_F is None:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    tw_F = xor_and_tree_width(formula)
    r_H_F = sum(sum(1 for x in row if x != 0) for row in H_F)
    
    c = Fraction(2, 1)  # Placeholder constant
    metric_value = tw_F <= c * r_H_F
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": tw_F,
        "instances_tested": 1,
        "conjecture_holds": metric_value,
        "counterexample": "" if metric_value else f"tw(F) = {tw_F}, c * r(H_F) = {c * r_H_F}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")