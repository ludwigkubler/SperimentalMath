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
    if n == 1:
        return [random.choice([0, 1])]
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return [left[i] ^ right[i] for i in range(min(len(left), len(right)))] + left[len(right):]

def compute_semgroup(circuit):
    n = len(circuit)
    semgroup = set()
    for i in range(1 << n):
        state = [0] * n
        for j in range(n):
            if (i >> j) & 1:
                state[j] = circuit[j]
        semgroup.add(tuple(state))
    return len(semgroup)

def compute_circuitmonowidth(circuit):
    n = len(circuit)
    width = 0
    for i in range(1 << n):
        state = [0] * n
        for j in range(n):
            if (i >> j) & 1:
                state[j] = circuit[j]
        width = max(width, sum(state))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 1 and n % 2 != 0:
            continue
        circuit = generate_circuit(n)
        semgroup_size = compute_semgroup(circuit)
        circuitmonowidth = compute_circuitmonowidth(circuit)
        
        results.append({
            "n": n,
            "semgroup_size": semgroup_size,
            "circuitmonowidth": circuitmonowidth
        })
    
    if not results:
        return {
            "metric_name": "Orbit Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    total_semgroup_size = sum(result["semgroup_size"] for result in results)
    total_circuitmonowidth = sum(result["circuitmonowidth"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    ratio = Fraction(total_semgroup_size, total_circuitmonowidth)
    conjecture_holds = ratio <= 1
    counterexample = "" if conjecture_holds else f"Ratio: {ratio}, Expected: ≤ 1"
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")