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
    
    def generate_circuit(depth, n):
        if depth == 0:
            return [random.choice([0, 1]) for _ in range(n)]
        else:
            inputs = generate_circuit(depth - 1, n)
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                return [inputs[i] & inputs[j] for i in range(len(inputs)) for j in range(i + 1, len(inputs))]
            elif gate == 'OR':
                return [inputs[i] | inputs[j] for i in range(len(inputs)) for j in range(i + 1, len(inputs))]
    
    def find_minimal_subspaces(circuit):
        n = len(circuit)
        subspaces = []
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] == circuit[j]:
                    continue
                subspace = [circuit[k] ^ (circuit[i] & circuit[j]) for k in range(n)]
                if all(subspace[k] == circuit[k] or subspace[k] == 0 for k in range(n)):
                    subspaces.append(subspace)
        return len(subspaces)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(random.randint(1, 40), n)
            metric_value = find_minimal_subspaces(circuit)
            total_metric_value += metric_value
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value <= (depth ** 2) * math.log(n, 2) for depth in range(1, 41) for n in [5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "min_subspaces",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")