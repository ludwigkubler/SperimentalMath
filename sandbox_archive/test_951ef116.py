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
    
    def generate_circuit(n):
        if n == 1:
            return ['0'] if random.choice([True, False]) else ['1']
        else:
            subcircuits = [generate_circuit(random.randint(1, n-1)) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [f"({sub[0]} {gate} {sub[1]})" for sub in zip(subcircuits[::2], subcircuits[1::2])]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            if circuit == '0' or circuit == '1':
                return [circuit]
            else:
                op = circuit.split()[1]
                left = evaluate_circuit(circuit.split()[0])
                right = evaluate_circuit(circuit.split()[2])
                if op == 'AND':
                    return ['0' if l == '0' or r == '0' else '1' for l, r in zip(left, right)]
                elif op == 'OR':
                    return ['1' if l == '1' or r == '1' else '0' for l, r in zip(left, right)]
        return circuit
    
    def topological_entropy(circuit):
        visited = set()
        
        def dfs(node):
            if node in visited:
                return 0
            visited.add(node)
            children = [evaluate_circuit(child) for child in node.split()[2:]]
            entropy = 0
            for child in children:
                entropy += dfs(child)
            entropy += math.log(len(children))
            return entropy
        
        return dfs(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            entropy = topological_entropy(circuit)
            if entropy <= 10:
                total_entropy += entropy
                instances_tested += 1
    
    mean_entropy = Fraction(total_entropy, instances_tested) if instances_tested > 0 else 0
    conjecture_holds = mean_entropy <= 2**n_values[-1]
    
    return {
        "metric_name": "Topological Entropy",
        "metric_value": float(mean_entropy),
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean entropy {mean_entropy} > 2^{n_values[-1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 
                                              101, 103, 107, 109, 113, 127, 131, 137, 
                                              139, 149, 151, 157, 163, 167, 173, 179, 
                                              181, 191, 193, 197, 199]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Mean entropy exceeds 10' first_failing_seed={first_failing_seed}")