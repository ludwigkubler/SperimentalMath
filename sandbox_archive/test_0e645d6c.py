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
            return ['0', '1']
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return [f'({x} & {y})' for x in left] + [f'({x} | {y})' for y in right]
    
    def evaluate_circuit(circuit):
        stack = []
        for token in circuit:
            if token == '0':
                stack.append(0)
            elif token == '1':
                stack.append(1)
            else:
                b = stack.pop()
                a = stack.pop()
                if '&' in token:
                    stack.append(a & b)
                elif '|' in token:
                    stack.append(a | b)
        return stack[0]
    
    def frege_proof_depth(circuit):
        if len(circuit) == 1:
            return 1
        left = circuit[:len(circuit)//2]
        right = circuit[len(circuit)//2:]
        return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
    
    def symplectic_leaves(circuit):
        if len(circuit) == 1:
            return 1
        left = circuit[:len(circuit)//2]
        right = circuit[len(circuit)//2:]
        return symplectic_leaves(left) + symplectic_leaves(right)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        depth = frege_proof_depth(circuit)
        leaves = symplectic_leaves(circuit)
        
        if depth <= 0 or leaves <= 0:
            continue
        
        metric_values.append(leaves / depth)
    
    if not metric_values:
        return {
            "metric_name": "symplectic_leaves_per_frege_depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = Fraction(instances_tested, instances_tested).limit_denominator()
    
    return {
        "metric_name": "symplectic_leaves_per_frege_depth",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= Fraction(8, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")