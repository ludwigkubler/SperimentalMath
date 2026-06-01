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

def calculate_tensor_representation(f, n):
    tensor = [[Fraction(f[i * (1 << j) + k], 2**(n - j)) for k in range(1 << j)] for j in range(n)]
    return tensor

def calculate_geometric_complexity(tensor):
    # Placeholder function to compute geometric complexity
    # This is a dummy implementation and should be replaced with actual GCT code
    n = len(tensor)
    return sum(sum(abs(x) for x in row) for row in tensor)

def calculate_communication_rank(f, n):
    # Placeholder function to compute communication rank
    # This is a dummy implementation and should be replaced with actual communication complexity code
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        instances_tested += n
        if instances_tested > 25:  # Avoid running too long
            break

        f = [random.randint(0, 1) for _ in range(1 << n)]
        tensor = calculate_tensor_representation(f, n)
        geometric_complexity = calculate_geometric_complexity(tensor)
        communication_rank = calculate_communication_rank(f, n)

        metric_values.append((geometric_complexity, communication_rank))
        n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "Geometric Complexity vs Communication Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_geometric_complexity = sum(x[0] for x in metric_values) / len(metric_values)
    std_geometric_complexity = math.sqrt(sum((x[0] - mean_geometric_complexity)**2 for x in metric_values) / len(metric_values))
    median_geometric_complexity = sorted([x[0] for x in metric_values])[len(metric_values) // 2]

    correlation_coefficient = sum((x[0] - mean_geometric_complexity) * (x[1] - mean_communication_rank) for x in metric_values)
    correlation_coefficient /= instances_tested * std_geometric_complexity * std_communication_rank

    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = "Correlation coefficient too low"

    return {
        "metric_name": "Geometric Complexity vs Communication Rank",
        "metric_value": mean_geometric_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_geometric_complexity = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_geometric_complexity = math.sqrt(sum((x["metric_value"] - mean_geometric_complexity)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_geometric_complexity} std={std_geometric_complexity} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")