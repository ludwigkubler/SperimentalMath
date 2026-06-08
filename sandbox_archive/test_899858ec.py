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
    
    def generate_circuit(n):
        if n == 0:
            return []
        elif n == 1:
            return [random.choice([0, 1])]
        else:
            left_size = random.randint(1, n-1)
            right_size = n - left_size
            left = generate_circuit(left_size)
            right = generate_circuit(right_size)
            return [left, right]
    
    def depth(circuit):
        if isinstance(circuit, list):
            return 1 + max(depth(subcircuit) for subcircuit in circuit)
        else:
            return 0
    
    def noncrossing_partition(circuit):
        if isinstance(circuit, list):
            left = noncrossing_partition(circuit[0])
            right = noncrossing_partition(circuit[1])
            return [left + right]
        else:
            return []
    
    def local_coherence_index(partition):
        if not partition:
            return 0
        return sum(len(subpartition) for subpartition in partition)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        depth_val = depth(circuit)
        partition = noncrossing_partition(circuit)
        msl = local_coherence_index(partition)
        
        if msl == 0 or depth_val == 0:
            continue
        
        results.append({
            "metric_name": "msl_over_depth",
            "metric_value": msl / depth_val,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False if msl > 3 * math.log(n) * depth_val else True,
            "counterexample": ""
        })
    
    mean_msl = sum(result["metric_value"] for result in results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_msl) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_msl_over_depth": mean_msl,
        "std_dev_msl_over_depth": std_dev,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_msl = sum(result["mean_msl_over_depth"] for result in results) / len(results)
    std_dev = sum(result["std_dev_msl_over_depth"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"msl > 3 * log(n) * depth(C)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")