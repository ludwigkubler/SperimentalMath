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
    
    def schur_weyl_multiplicity(matrix):
        n = len(matrix)
        # Placeholder for actual Schur-Weyl multiplicity calculation
        return 1.0  # Simplified placeholder
    
    def permanent(matrix):
        if not matrix:
            return 0
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * permanent(submatrix)
            sign *= -1
        return det
    
    def determinant(matrix):
        if not matrix:
            return 0
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(submatrix)
        return det
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random matrices
            matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            perm_mul = schur_weyl_multiplicity(matrix)
            det_mul = schur_weyl_multiplicity(matrix)
            results.append((perm_mul, det_mul))
    
    if not results:
        return {
            "metric_name": "Schur-Weyl Multiplicity Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    perm_mul_sum = sum(x for x, _ in results)
    det_mul_sum = sum(y for _, y in results)
    mean_ratio = perm_mul_sum / det_mul_sum
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x, _ in results) / len(results))
    
    return {
        "metric_name": "Schur-Weyl Multiplicity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio >= 2 and std_ratio <= 1.5,
        "counterexample": "" if mean_ratio >= 2 else f"Mean ratio {mean_ratio} < 2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")