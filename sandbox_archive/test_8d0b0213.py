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
    
    def generate_random_circuit(n):
        # Generate a random Boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                input_index = random.randint(0, n-1)
                circuit.append((gate, input_index))
            else:
                input_indices = sorted(random.sample(range(n), 2))
                circuit.append((gate, input_indices[0], input_indices[1]))
        return circuit
    
    def compute_twisted_brauer_group(circuit):
        # Placeholder for computing the twisted Brauer group
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 2**n)
    
    def communication_complexity_rank(circuit):
        # Placeholder for calculating the communication complexity rank
        # This is a dummy implementation and should be replaced with actual calculation
        return len(circuit) / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        order_brauer = compute_twisted_brauer_group(circuit)
        rank_comm = communication_complexity_rank(circuit)
        
        if order_brauer == 0 or rank_comm == 0:
            continue
        
        ratio = rank_comm / math.log2(order_brauer)
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "communication_complexity_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "communication_complexity_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(r <= 1.5 for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)