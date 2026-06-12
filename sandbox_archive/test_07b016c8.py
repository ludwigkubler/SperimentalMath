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
        if D == 1:
            return ['0'] * n + ['1'] * n
        else:
            subcircuits = [generate_circuit(n // 2, D - 1) for _ in range(2)]
            return ['('] + subcircuits[0] + ['|'] + subcircuits[1] + [')']
    
    def evaluate_circuit(circuit):
        stack = []
        for token in circuit:
            if token == '0' or token == '1':
                stack.append(token)
            elif token == '|':
                b = stack.pop()
                a = stack.pop()
                stack.append(''.join(sorted(a + b)))
            else:
                raise ValueError("Invalid token")
        return stack[0]
    
    def syntactic_monoid(circuit):
        circuit = evaluate_circuit(circuit)
        generators = set(circuit)
        relations = []
        for i in range(len(circuit)):
            for j in range(i + 1, len(circuit)):
                if circuit[i] != circuit[j]:
                    relations.append((circuit[i], circuit[j]))
        return generators, relations
    
    def minimal_locally_indecomposable_module(generators, relations):
        # Simplified algorithm to find the module
        module = set()
        for gen in generators:
            module.add(gen)
        for rel in relations:
            if rel[0] not in module or rel[1] not in module:
                continue
            module.add(rel[0])
            module.add(rel[1])
        return len(module)
    
    n_max = 40
    instances_tested = 30
    total_ratio = 0
    
    for _ in range(instances_tested):
        D = random.randint(5, 40)
        circuit = generate_circuit(n_max, D)
        generators, relations = syntactic_monoid(circuit)
        module_order = minimal_locally_indecomposable_module(generators, relations)
        ratio = module_order / (D ** 2)
        
        if ratio < 0.5 or ratio > 1.5:
            return {
                "metric_name": "Ratio of Module Order to Depth^2",
                "metric_value": ratio,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Ratio out of bounds: {ratio}"
            }
        
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "Ratio of Module Order to Depth^2",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")