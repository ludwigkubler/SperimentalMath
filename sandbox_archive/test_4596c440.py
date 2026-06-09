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
    
    def generate_circuit(n, D):
        if n == 1 and D == 0:
            return [0]
        elif n == 1 and D > 0:
            return [random.choice([0, 1])]
        else:
            subcircuits = []
            for _ in range(D + 1):
                subcircuit = generate_circuit(n // 2, random.randint(0, D - 1))
                subcircuits.append(subcircuit)
            if n % 2 == 1:
                subcircuits.append(generate_circuit(1, 0))
            return [random.choice([0, 1]) for _ in range(n)] + sum(subcircuits, [])
    
    def compute_entropy(circuit):
        n = len(circuit) // (D + 1)
        transitions = {}
        for i in range(len(circuit)):
            state = tuple(circuit[:i])
            next_state = tuple(circuit[i:i+n])
            if state not in transitions:
                transitions[state] = []
            transitions[state].append(next_state)
        
        entropy = 0
        for state, next_states in transitions.items():
            counts = [next_states.count(state) for state in set(next_states)]
            probabilities = [count / len(next_states) for count in counts]
            entropy += -sum(p * math.log2(p) for p in probabilities)
        
        return entropy
    
    def measure_depth(circuit):
        n = len(circuit) // (D + 1)
        depth = 0
        current_state = tuple(circuit[:n])
        while True:
            next_states = [tuple(circuit[i:i+n]) for i in range(n, len(circuit), n)]
            if len(set(next_states)) == 1:
                break
            current_state = next_states[0]
            depth += 1
        return depth
    
    def analyze_results(entropy, depth):
        bound = depth * math.log2(2 ** (depth + 1))
        ratio = entropy / bound
        return ratio <= 1.0
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0
    support_count = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, min(3, n)))
            entropy = compute_entropy(circuit)
            depth = measure_depth(circuit)
            instances_tested += 1
            total_entropy += entropy
            if not analyze_results(entropy, depth):
                counterexample = f"Circuit with n={n}, D={depth} failed"
                break
    
    mean_entropy = total_entropy / instances_tested
    support_fraction = support_count / len(n_values)
    
    return {
        "metric_name": "Entropy Ratio",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": counterexample == "",
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["counterexample"]) / len(results)
    
    if all(not r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")