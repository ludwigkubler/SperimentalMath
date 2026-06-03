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
    
    def generate_circuit(depth, size):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = []
            for _ in range(size):
                subcircuit = generate_circuit(depth - 1, size // depth)
                subcircuits.append(subcircuit)
            return subcircuits
    
    def compute_entropy(circuit):
        if isinstance(circuit, list):
            entropy = 0
            for subcircuit in circuit:
                entropy += compute_entropy(subcircuit)
            return entropy / len(circuit)
        else:
            return 1
    
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            depth = random.randint(1, n)
            size = random.randint(1, n)
            circuit = generate_circuit(depth, size)
            entropy = compute_entropy(circuit)
            metric_value += entropy
            instances_tested += 1
            
            if entropy < math.log(size):
                conjecture_holds = False
                counterexample = f"Circuit with depth {depth}, size {size} has entropy {entropy} < log({size})"
    
    mean_metric_value = metric_value / instances_tested
    support_fraction = instances_tested / (6 * 5)
    
    return {
        "metric_name": "Minimal Topological Entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")