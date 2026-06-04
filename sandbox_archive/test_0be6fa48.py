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

def generate_monotone_circuit(n, w):
    circuit = []
    for _ in range(w):
        row = [0] * n
        for i in range(n):
            if random.choice([True, False]):
                row[i] = 1
        circuit.append(row)
    return circuit

def compute_minimal_order(circuit):
    n = len(circuit[0])
    order = []
    for i in range(n):
        if all(row[i] == 1 for row in circuit):
            order.append(1)
        else:
            order.append(0)
    return sum(order)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_circuit(n, n // 2)
        order = compute_minimal_order(circuit)
        results.append(order)
    
    mean_order = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_order) ** 2 for x in results) / len(results))
    conjecture_holds = all(abs(x - (n // 2) ** 2) <= 10 for n, x in zip(n_values, results))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"order={max(results)} exceeds expected O(w(C)^2)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - (n // 2) ** 2) > 10 for n, result in zip(n_values, results)):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - (n // 2) ** 2) > 10)
        print(f"RESULT: FALSIFIED counterexample='order exceeds expected O(w(C)^2)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")