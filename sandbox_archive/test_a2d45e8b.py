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


def generate_random_circuit(n):
    if n == 1:
        return random.choice([0, 1])
    else:
        left = generate_random_circuit(n // 2)
        right = generate_random_circuit(n - n // 2)
        return (left, right)


def state_space_representation(circuit):
    if isinstance(circuit, int):
        return {circuit}
    else:
        left_states = state_space_representation(circuit[0])
        right_states = state_space_representation(circuit[1])
        return {x ^ y for x in left_states for y in right_states}


def minimal_polynomial(state_space, m):
    if not state_space:
        return 0
    poly = [1]
    for s in state_space:
        new_poly = []
        for coeff in poly:
            new_poly.append(coeff * s)
        poly.extend(new_poly)
    return poly


def topological_entropy(state_space):
    n = len(state_space)
    if n == 0:
        return 0
    log_n = math.log2(n)
    entropy = -sum(1 / n * math.log2(1 / n) for _ in range(n))
    return entropy


def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_entropy = 0
        total_log_m = 0
        for _ in range(30):
            circuit = generate_random_circuit(n)
            state_space = state_space_representation(circuit)
            m = len(state_space) - 1
            if m == 0:
                continue
            poly = minimal_polynomial(state_space, m)
            entropy = topological_entropy(state_space)
            total_entropy += entropy
            total_log_m += math.log2(m)
            instances_tested += 1
        if instances_tested < 30:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        mean_entropy = total_entropy / instances_tested
        mean_log_m = total_log_m / instances_tested
        covariance = sum((entropy - mean_entropy) * (math.log2(m) - mean_log_m) for entropy, m in zip(results, range(5, 41))) / instances_tested
        variance_m = sum((math.log2(m) - mean_log_m) ** 2 for m in range(5, 41)) / instances_tested
        correlation_coefficient = covariance / math.sqrt(variance_m * instances_tested)
        results.append(correlation_coefficient)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": sum(results) / len(results),
        "instances_tested": 30 * len(results),
        "n_max": 40,
        "conjecture_holds": abs(sum(results) / len(results)) >= 0.7,
        "counterexample": ""
    }


if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) >= 0.7) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r) < 0.5 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.5))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")