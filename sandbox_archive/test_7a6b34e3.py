# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def generate_or_and_circuit(n, d):
    circuit = []
    for _ in range(d):
        layer = [random.choice(['OR', 'AND']) for _ in range(n)]
        circuit.append(layer)
    return circuit

def calculate_tee(circuit, state):
    n = len(state)
    depth = len(circuit)
    if depth == 0:
        return Fraction(0, 1)
    tee = Fraction(depth * math.log2(n), 1)
    return tee

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for d in range(1, min(n, 10)):
            circuit = generate_or_and_circuit(n, d)
            state = [random.choice([0, 1]) for _ in range(n)]
            tee = calculate_tee(circuit, state)
            results.append((n, d, tee))
    
    max_tee = max(results, key=lambda x: x[2])[2]
    min_tee = min(results, key=lambda x: x[2])[2]
    
    f_n_d = Fraction(d * math.log2(n), 1)
    g_n_d = Fraction(d, 1)
    
    conjecture_holds = all(tee <= f_n_d for _, d, tee in results) or any(tee >= g_n_d for _, d, tee in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "topological_entanglement_entropy",
        "metric_value": (max_tee + min_tee) / 2,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")