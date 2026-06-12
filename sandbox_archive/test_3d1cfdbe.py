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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_circuit(depth):
    if depth == 0:
        return "input"
    else:
        inputs = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
        operation = random.choice(["and", "or"])
        return f"({inputs[0]} {operation} {inputs[1]})"

def calculate_quandle_rank(circuit):
    if circuit == "input":
        return 1
    else:
        left, _, right = circuit.split()
        rank_left = calculate_quandle_rank(left)
        rank_right = calculate_quandle_rank(right)
        return max(rank_left, rank_right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depth_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    depths = []

    for depth in depth_values:
        circuit = generate_circuit(depth)
        rank = calculate_quandle_rank(circuit)
        ranks.append(rank)
        depths.append(depth)

    correlation_coefficient = sum((ranks[i] - sum(ranks) / len(ranks)) * (depths[i] - sum(depths) / len(depths)) for i in range(len(ranks))) / (len(ranks) * sum((ranks[i] - sum(ranks) / len(ranks)) ** 2 for i in range(len(ranks)))) if len(ranks) > 1 else None

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(depth_values),
        "n_max": max(depth_values),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if correlation_coefficient is not None and abs(correlation_coefficient) >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, result in enumerate(results) if not result['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_budget_exceeded")