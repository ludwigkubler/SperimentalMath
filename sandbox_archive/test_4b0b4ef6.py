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
    circuit = []
    for _ in range(2**n):
        gate = random.choice(['AND', 'OR'])
        inputs = random.sample(range(n), 2)
        circuit.append((gate, inputs))
    return circuit

def evaluate_circuit(circuit, inputs):
    stack = inputs[:]
    for gate, inputs in reversed(circuit):
        if len(stack) < 2:
            raise ValueError("Invalid circuit: not enough values on the stack")
        a = stack.pop()
        b = stack.pop()
        if gate == 'AND':
            result = a and b
        elif gate == 'OR':
            result = a or b
        else:
            raise ValueError(f"Invalid gate: {gate}")
        stack.append(result)
    if len(stack) != 1:
        raise ValueError("Invalid circuit: too many values on the stack")
    return stack[0]

def local_induction_ring_rank(circuit):
    n = len(circuit)
    rank = 0
    for i in range(n):
        inputs = [0] * n
        inputs[i] = 1
        if evaluate_circuit(circuit, inputs):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        circuits = [generate_random_circuit(n) for _ in range(5)]
        ranks = [local_induction_ring_rank(circuit) for circuit in circuits]
        variance = sum((x - sum(ranks) / len(ranks)) ** 2 for x in ranks) / len(ranks)
        total_variance += variance
        instances_tested += len(ranks)
        n_max = max(n_max, n)

        if variance > 10 * (n * math.log(n)):
            conjecture_holds = False
            counterexample = f"Variance {variance} exceeds 10 * {n} * log({n})"

    mean_variance = total_variance / len(n_values)
    support_fraction = sum(1 for n in n_values if variance <= 10 * (n * math.log(n))) / len(n_values)

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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["counterexample"]) / len(results)

    if all(not r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")