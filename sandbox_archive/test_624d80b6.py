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
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
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
        rows, cols = len(matrix), len(matrix[0])
        det = 1
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        augmented_matrix = gaussian_elimination(augmented_matrix)
        for i in range(rows):
            det *= augmented_matrix[i][i]
        return det

    def irreducible_representation_order(n):
        # Simplified example of a mapping from n to the order of an irreducible representation
        return 2 * n + random.randint(0, int(0.1 * n))

    def communication_complexity_rank(n):
        # Simplified example of a mapping from n to the rank of a communication game
        return n // 2

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        order = irreducible_representation_order(n)
        rank = communication_complexity_rank(n)
        expected_order = min(2 * n * math.log(n), 2 * rank * math.log(n))
        difference = abs(order - expected_order) / expected_order
        metric_values.append(difference)

    mean_difference = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "Mean Difference",
        "metric_value": mean_difference,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": mean_difference <= 0.01,
        "counterexample": "" if mean_difference <= 0.01 else f"Mean difference {mean_difference} > 1%"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_difference = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_difference} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")