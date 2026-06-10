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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return (gate, inputs)

    def compute_matroid(circuit):
        if not circuit:
            return set()
        gate, inputs = circuit
        matroid = set(inputs)
        for input_circuit in inputs:
            matroid.update(compute_matroid(input_circuit))
        return matroid

    def local_induction_degree(matroid):
        n = len(matroid)
        if n == 0:
            return 0
        max_independent_set_size = 0
        for i in range(1 << n):
            independent_set = [j for j in range(n) if (i & (1 << j)) != 0]
            if all(len(matroid.intersection(set(independent_set[:k]))) == k-1 for k in range(2, len(independent_set)+1)):
                max_independent_set_size = max(max_independent_set_size, len(independent_set))
        return n - max_independent_set_size

    def entanglement_complexity(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit
        return sum(entanglement_complexity(input_circuit) for input_circuit in inputs)

    depth_values = [5, 10, 15, 20, 30, 40]
    entanglement_complexity_values = []
    lidb_values = []

    for n in depth_values:
        circuit = generate_random_circuit(n)
        matroid = compute_matroid(circuit)
        lidb = local_induction_degree(matroid)
        entanglement_complexity_value = entanglement_complexity(circuit)
        entanglement_complexity_values.append(entanglement_complexity_value)
        lidb_values.append(lidb)

    correlation_coefficient = 0
    n_max = max(depth_values)
    instances_tested = len(depth_values)
    conjecture_holds = False
    counterexample = ""

    if instances_tested >= 30:
        mean_entanglement_complexity = sum(entanglement_complexity_values) / instances_tested
        mean_lidb = sum(lidb_values) / instances_tested

        # Calculate the correlation coefficient
        covariance = sum((entanglement_complexity_values[i] - mean_entanglement_complexity) * (lidb_values[i] - mean_lidb) for i in range(instances_tested))
        variance_entanglement = sum((entanglement_complexity_values[i] - mean_entanglement_complexity) ** 2 for i in range(instances_tested))
        variance_lidb = sum((lidb_values[i] - mean_lidb) ** 2 for i in range(instances_tested))

        if variance_entanglement > 0 and variance_lidb > 0:
            correlation_coefficient = covariance / math.sqrt(variance_entanglement * variance_lidb)

    if correlation_coefficient >= 0.8:
        conjecture_holds = True

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "correlation_coefficient < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")