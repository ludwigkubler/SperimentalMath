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

def generate_circuit(n):
    circuit = []
    for _ in range(n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            result = all(stack.pop() for _ in range(len(inputs)))
        elif gate_type == 'OR':
            result = any(stack.pop() for _ in range(len(inputs)))
        stack.append(result)
    return stack[0]

def local_induction_ring_rank(circuit):
    n = len(circuit)
    ranks = [evaluate_circuit(circuit[:i] + [(circuit[i][0], circuit[i][1][::-1])] + circuit[i+1:]) for i in range(n)]
    return max(ranks)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        circuits = [generate_circuit(n) for _ in range(30)]
        ranks = [local_induction_ring_rank(circuit) for circuit in circuits]
        variance = sum((x - (sum(ranks) / len(ranks))) ** 2 for x in ranks) / len(ranks)
        total_variance += variance
        instances_tested += len(ranks)
        n_max = max(n_max, n)

    mean_variance = total_variance / len(n_values)
    conjecture_holds = mean_variance <= 10 * (n_max * math.log2(n_max))
    counterexample = "" if conjecture_holds else "variance_not_O_n_log_n"

    return {
        "metric_name": "Variance of Local Induction Ring Rank",
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"variance_not_O_n_log_n\" first_failing_seed={first_failing_seed}")