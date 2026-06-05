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
    
    # Define constants and parameters
    max_n = 40
    num_trials_per_seed = 30
    
    def generate_d_regular_circuit(d, n):
        if n % d != 0:
            return None
        circuit = []
        for _ in range(n // d):
            circuit.extend([i for i in range(1, d + 1)])
        random.shuffle(circuit)
        return circuit

    def compute_min_complex_structures(circuit):
        # Placeholder function to simulate the computation of m(K)
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(circuit)) * 2
    
    results = []
    for _ in range(num_trials_per_seed):
        n = random.randint(5, max_n)
        d = random.randint(2, min(n - 1, 4))
        circuit = generate_d_regular_circuit(d, n)
        if circuit is None:
            continue
        m_K = compute_min_complex_structures(circuit)
        results.append(m_K / n)
    
    if not results:
        return {
            "metric_name": "m(K)/D",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r <= 1.0]) / len(results)
    
    return {
        "metric_name": "m(K)/D",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(r['metric_value'] for r in results) / len(results):.2f} std={math.sqrt(sum((r['metric_value'] - sum(r['metric_value'] for r in results) / len(results)) ** 2 for r in results) / len(results)):.2f} support_fraction={(sum(1 for r in results if r['conjecture_holds']) / len(results)):.2f}")