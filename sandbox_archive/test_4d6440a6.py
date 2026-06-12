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

def generate_random_circuit(m, d):
    if m <= 0 or d <= 0:
        return None
    circuit = []
    for _ in range(d):
        layer = [random.choice(['AND', 'OR']) for _ in range(m)]
        circuit.append(layer)
    return circuit

def evaluate_circuit(circuit):
    if not circuit:
        return False
    stack = []
    inputs = [False] * len(circuit[-1])
    for layer in reversed(circuit):
        new_stack = []
        for gate in layer:
            if gate == 'AND':
                a = stack.pop()
                b = stack.pop()
                new_stack.append(a and b)
            elif gate == 'OR':
                a = stack.pop()
                b = stack.pop()
                new_stack.append(a or b)
        stack = new_stack
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [5, 10, 15, 20, 30, 40]
    fpd_values = []
    shv_values = []

    for n in range(30):
        circuit = generate_random_circuit(m_values[n], n + 1)
        if not circuit:
            continue
        result = evaluate_circuit(circuit)
        fpd_values.append(n + 1)
        shv_values.append(result)  # Simplified SHV as a boolean value

    if len(fpd_values) < 30 or len(shv_values) < 30:
        return {
            "metric_name": "SHV vs FPD",
            "metric_value": None,
            "instances_tested": len(fpd_values),
            "n_max": max(fpd_values) if fpd_values else 0,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean_fpd = sum(fpd_values) / len(fpd_values)
    mean_shv = sum(shv_values) / len(shv_values)
    std_dev_fpd = math.sqrt(sum((x - mean_fpd) ** 2 for x in fpd_values) / len(fpd_values))
    std_dev_shv = math.sqrt(sum((x - mean_shv) ** 2 for x in shv_values) / len(shv_values))

    correlation_coefficient = sum((fpd_values[i] - mean_fpd) * (shv_values[i] - mean_shv) for i in range(len(fpd_values))) / (len(fpd_values) * std_dev_fpd * std_dev_shv)

    return {
        "metric_name": "SHV vs FPD",
        "metric_value": correlation_coefficient,
        "instances_tested": len(fpd_values),
        "n_max": max(fpd_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_shv / mean_fpd - 1) <= std_dev_shv / std_dev_fpd,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")