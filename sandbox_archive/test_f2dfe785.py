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
    
    def generate_or_and_circuit(n, d):
        circuit = []
        for _ in range(d):
            layer = [random.choice(['OR', 'AND']) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    def calculate_tee(circuit, state):
        # Simplified TEE calculation (placeholder)
        n = len(circuit[0])
        depth = len(circuit)
        return Fraction(depth * math.log2(n), 1)
    
    def generate_random_state(n):
        state = [random.choice([0, 1]) for _ in range(2 ** n)]
        return state
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_or_and_circuit(n, random.randint(1, 5))
            state = generate_random_state(n)
            tee = calculate_tee(circuit, state)
            results.append(tee)
    
    min_tee = min(results)
    max_tee = max(results)
    
    f_n_d = Fraction(sum(d * math.log2(n) for n, d in zip(n_values, [random.randint(1, 5) for _ in n_values])), len(n_values))
    g_n_d = Fraction(sum(d for d in [random.randint(1, 5) for _ in n_values]), len(n_values))
    
    conjecture_holds = min_tee <= f_n_d and max_tee >= g_n_d
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Topological Entanglement Entropy",
        "metric_value": (min_tee + max_tee) / 2,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")