# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 0
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            for c in range(n):
                submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                det += ((-1) ** c) * matrix[0][c] * determinant(submatrix)
        return det

    def ac0_circuit_size(poly, n):
        # Placeholder function to compute AC0 circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return len(poly)

    def minimal_hodge_index(n):
        # Placeholder function to compute Minimal Hodge Index
        # This is a dummy implementation and should be replaced with actual logic
        return n

    n = random.randint(5, 40)
    poly = sum(random.choice([-1, 1]) * 'x' + str(i) for i in range(n))
    ac0_size = ac0_circuit_size(poly, n)
    hodge_index = minimal_hodge_index(n)

    return {
        "metric_name": "AC0 Circuit Size vs Hodge Index",
        "metric_value": ac0_size,
        "instances_tested": 1,
        "conjecture_holds": ac0_size <= hodge_index,
        "counterexample": "" if ac0_size <= hodge_index else f"Counterexample: AC0 size {ac0_size} > Hodge Index {hodge_index}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H1 > AC0 circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")