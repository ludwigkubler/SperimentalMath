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
    
    def generate_circuit(n, depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_circuit(n, depth - 1) for _ in range(2)]
            return (gate, inputs)
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, int):
            return circuit
        gate, inputs = circuit
        if gate == 'AND':
            return evaluate_circuit(inputs[0]) and evaluate_circuit(inputs[1])
        elif gate == 'OR':
            return evaluate_circuit(inputs[0]) or evaluate_circuit(inputs[1])
    
    def topological_entropy(circuit):
        visited = set()
        
        def dfs(node):
            if node in visited:
                return 0
            visited.add(node)
            entropy = 0
            for child in circuit[node]:
                entropy += dfs(child)
            return entropy + 1
        
        return dfs(0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(2, n))
            entropy = topological_entropy(circuit)
            results.append((n, entropy))
    
    if len(results) < 30:
        return {
            "metric_name": "topological_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_entropy = sum(entropy for _, entropy in results) / len(results)
    if mean_entropy > 10:
        return {
            "metric_name": "topological_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": f"mean_entropy={mean_entropy} > 10"
        }
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")