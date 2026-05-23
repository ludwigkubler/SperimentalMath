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
    
    def generate_boolean_algebra(n):
        elements = [f"x{i}" for i in range(2**n)]
        operations = {}
        for a in elements:
            for b in elements:
                if a == b:
                    operations[(a, b)] = a
                else:
                    operations[(a, b)] = f"{a} ∨ {b}"
        return operations
    
    def compute_crossed_product_rank(operations):
        # Simplified rank computation (not actual crossed product)
        return len(operations) ** 0.5
    
    def generate_ac0_circuit(n):
        size = 2**math.ceil(math.log2(n))
        circuit = []
        for _ in range(size):
            gate = random.choice(["AND", "OR"])
            inputs = [random.choice([f"x{i}" for i in range(2**n)]) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_circuit_size(circuit):
        size = 0
        for gate, _ in circuit:
            if gate == "AND":
                size += len(_)
            elif gate == "OR":
                size += len(_)
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        B = generate_boolean_algebra(n)
        ψ_B = compute_crossed_product_rank(B)
        C = generate_ac0_circuit(n)
        size_C = compute_circuit_size(C)
        
        if size_C == 0:
            continue
        
        results.append(ψ_B / math.log(size_C))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": all(x >= mean + 3 * std_dev for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 6)]  # Default to first few primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= mean + 3 * std_dev) / len(results)
    
    if all(x >= mean + 3 * std_dev for x in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(x < mean + 3 * std_dev for x in results):
        first_failing_seed = seeds[results.index(next(x for x in results if x < mean + 3 * std_dev))]
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")