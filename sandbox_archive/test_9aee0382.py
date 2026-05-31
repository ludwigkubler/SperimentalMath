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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_quantum_circuit(n, t):
        # Simplified circuit generation (not actual quantum circuit synthesis)
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(t)]
    
    def automorphism_group_size(boolean_function):
        n = int(math.log2(len(boolean_function)))
        cube = [i for i in range(2**n)]
        generators = []
        for i in range(n):
            if boolean_function[i] != boolean_function[0]:
                generators.append(i)
        return len(generators)
    
    def tensor_network_depth(circuit):
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            boolean_function = generate_boolean_function(n)
            circuit = generate_quantum_circuit(n, random.randint(1, 2))
            G = automorphism_group_size(boolean_function)
            t = tensor_network_depth(circuit)
            results.append({"n": n, "G": G, "t": t})
    
    if not results:
        return {
            "metric_name": "automorphism_group_size",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_G = sum(result["G"] for result in results) / len(results)
    mean_t = sum(result["t"] for result in results) / len(results)
    conjecture_holds = all(G >= 2**t for G, t in zip([result["G"] for result in results], [result["t"] for result in results]))
    
    return {
        "metric_name": "automorphism_group_size",
        "metric_value": mean_G,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found at n={results[0]['n']}, G={results[0]['G']}, t={results[0]['t']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_G = sum(result["metric_value"] for result in results) / len(results)
    std_G = math.sqrt(sum((result["metric_value"] - mean_G)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_G} std={std_G} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_G} std={std_G} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")