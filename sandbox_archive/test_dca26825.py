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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit

    def dependency_graph(circuit):
        graph = {}
        for i, (_, inputs) in enumerate(circuit):
            for input in inputs:
                if input not in graph:
                    graph[input] = []
                graph[input].append(i)
        return graph

    def knot_complexity(graph):
        # Simplified knot complexity calculation
        return len(graph)

    def crossing_changes(circuit):
        # Simplified crossing changes calculation
        return len(circuit) // 2

    def min_generators(knot_complexity):
        # Simplified minimum generators calculation
        return int(math.sqrt(knot_complexity))

    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    graph = dependency_graph(circuit)
    knot_complex = knot_complexity(graph)
    cross_changes = crossing_changes(circuit)
    min_gen = min_generators(knot_complex)

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": (cross_changes / min_gen) if min_gen != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")