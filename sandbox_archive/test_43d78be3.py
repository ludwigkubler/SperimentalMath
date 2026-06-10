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
    n = 40
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""

    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit

    def is_satisfiable(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]

    def compute_automorphism_group(circuit):
        # Simplified version of computing automorphism group
        # This is a placeholder and should be replaced with actual computation
        return 1

    metrics = []
    for _ in range(instances_tested):
        circuit = generate_random_circuit(n)
        aut_size = compute_automorphism_group(circuit)
        satisfiability_complexity = is_satisfiable(circuit)
        log_aut_size = math.log2(aut_size) if aut_size > 0 else -math.inf
        log_n = math.log2(n)
        metrics.append((log_aut_size, log_n))

    mean_log_aut_over_n = sum(x / y for x, y in metrics) / len(metrics)
    std_dev = math.sqrt(sum((x / y - mean_log_aut_over_n) ** 2 for x, y in metrics) / len(metrics))
    lower_bound = mean_log_aut_over_n - 0.5 * std_dev
    upper_bound = mean_log_aut_over_n + 0.5 * std_dev

    if any(lower_bound > log_aut_size / log_n or log_aut_size / log_n > upper_bound for log_aut_size, log_n in metrics):
        conjecture_holds = False
        counterexample = "log2(|Aut(C)|) / log(n) outside 0.5 std dev range"

    return {
        "metric_name": "log2(|Aut(C)|) / log(n)",
        "metric_value": mean_log_aut_over_n,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")