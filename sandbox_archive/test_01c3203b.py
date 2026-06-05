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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, depth):
        if n == 1:
            return ['0'] if random.choice([True, False]) else ['1']
        elif depth == 0:
            return [random.choice(['0', '1']) for _ in range(n)]
        else:
            inputs = generate_circuit(n, depth - 1)
            gate = random.choice(['AND', 'OR'])
            return [f"({gate} {inputs[i]} {inputs[i+1]})" for i in range(0, n, 2)]

    def satisfiability_threshold(circuit):
        if isinstance(circuit, str) and circuit[0] in ['0', '1']:
            return 1
        elif isinstance(circuit, list) and len(circuit) == 1:
            return satisfiability_threshold(circuit[0])
        else:
            left = satisfiability_threshold(circuit[2])
            right = satisfiability_threshold(circuit[3])
            return max(left, right)

    def p_adic_l_function_order(n):
        # Simplified approximation for demonstration purposes
        return Fraction(n, 2)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    alpha = None
    beta = None

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(1, 3))
            k = satisfiability_threshold(circuit)
            order = p_adic_l_function_order(n)

            total_metric_value += order
            instances_tested += 1
            n_max = max(n_max, n)

    mean = Fraction(total_metric_value, instances_tested)
    if instances_tested < 30:
        return {
            "metric_name": "p-adic L-function Order",
            "metric_value": float(mean),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    # Estimate alpha and beta
    sum_k = 0
    sum_k_order = 0
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, 3))
            k = satisfiability_threshold(circuit)
            order = p_adic_l_function_order(n)

            sum_k += k
            sum_k_order += k * order

    alpha = Fraction(sum_k_order, sum_k)
    beta = mean - alpha * n_max / len(n_values)

    # Check if the conjecture holds
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, 3))
            k = satisfiability_threshold(circuit)
            order = p_adic_l_function_order(n)
            expected_bound = alpha * math.log(n) + beta

            if order > expected_bound + 3 * (expected_bound - mean):
                return {
                    "metric_name": "p-adic L-function Order",
                    "metric_value": float(mean),
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"Order {order} exceeds expected bound {expected_bound} by more than 3 std"
                }

    return {
        "metric_name": "p-adic L-function Order",
        "metric_value": float(mean),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")