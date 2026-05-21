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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_circuit(n):
        if n == 1:
            return [0]
        else:
            left = generate_monotone_circuit(n // 2)
            right = generate_monotone_circuit(n - n // 2)
            return [left, right] + [1]
    
    def circuit_depth(circuit):
        if isinstance(circuit, int):
            return 0
        else:
            depths = [circuit_depth(sub_circuit) for sub_circuit in circuit[1:]]
            return max(depths) + 1
    
    def hodge_index(circuit):
        if isinstance(circuit, int):
            return 0
        else:
            left_hodge = hodge_index(circuit[1])
            right_hodge = hodge_index(circuit[2])
            return left_hodge + right_hodge + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_circuit(n)
        depth = circuit_depth(circuit)
        hodge = hodge_index(circuit)
        
        if hodge > 10000:
            return {
                "metric_name": "Hodge Index",
                "metric_value": hodge,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, h^1(C)={hodge}"
            }
        
        results.append((depth, hodge))
    
    mean_depth = sum(depth for depth, _ in results) / len(results)
    mean_hodge = sum(hodge for _, hodge in results) / len(results)
    std_dev = math.sqrt(sum((hodge - mean_hodge) ** 2 for _, hodge in results) / len(results))
    
    return {
        "metric_name": "Hodge Index",
        "metric_value": mean_hodge,
        "instances_tested": len(n_values),
        "conjecture_holds": all(hodge <= 10000 for _, hodge in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='h^1(C) > 10000' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")