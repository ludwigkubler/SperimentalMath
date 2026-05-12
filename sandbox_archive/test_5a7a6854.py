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

def generate_symmetric_block_design(v, k, lambda_):
    if v * (v - 1) % (2 * k) != 0:
        return None
    blocks = []
    points = list(range(v))
    for _ in range(k):
        block = random.sample(points, k)
        if all(len(set(block).intersection(other)) == lambda_ for other in blocks):
            blocks.append(block)
        else:
            return None
    return blocks

def construct_communication_matrix(blocks):
    n = len(blocks)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            common_points = set(blocks[i]).intersection(blocks[j])
            matrix[i][j] = matrix[j][i] = len(common_points)
    return matrix

def discrepancy(matrix):
    n = len(matrix)
    max_discrepancy = 0
    for i in range(n):
        row_sum = sum(matrix[i])
        col_sum = sum(matrix[j][i] for j in range(n))
        max_discrepancy = max(max_discrepancy, abs(row_sum - col_sum))
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    v = random.choice([10, 15, 20, 30, 40])
    k = random.randint(2, v // 2)
    lambda_ = random.randint(1, min(k - 1, v - k))
    design = generate_symmetric_block_design(v, k, lambda_)
    if not design:
        return {
            "metric_name": "discrepancy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "design_not_possible"
        }
    matrix = construct_communication_matrix(design)
    disc = discrepancy(matrix)
    lower_bound = math.sqrt(lambda_ * v / k)
    return {
        "metric_name": "discrepancy",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": disc >= lower_bound,
        "counterexample": "" if disc >= lower_bound else f"disc={disc} < {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")