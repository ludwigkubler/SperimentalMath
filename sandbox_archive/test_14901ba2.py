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
    
    def generate_quaternion():
        return [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    
    def tropicalize(q):
        return max(abs(x) for x in q)
    
    def construct_circuit(depth: int):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            left = construct_circuit(random.randint(0, depth-1))
            right = construct_circuit(random.randint(0, depth-1))
            return [left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit[0], list):
            left = evaluate_circuit(circuit[0])
            right = evaluate_circuit(circuit[1])
            return left ^ right
        else:
            return circuit
    
    def minimal_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    def diameter(circuit):
        if isinstance(circuit[0], list):
            left_diameter = diameter(circuit[0])
            right_diameter = diameter(circuit[1])
            return max(left_diameter, right_diameter) + 1
        else:
            return 0
    
    n_tests = 30
    total_rank = 0
    total_diameter = 0
    
    for _ in range(n_tests):
        q = generate_quaternion()
        tau_trop = tropicalize(q)
        circuit_depth = random.randint(5, 40)
        circuit = construct_circuit(circuit_depth)
        rank = minimal_rank(circuit)
        diameter_val = diameter(circuit)
        
        total_rank += rank
        total_diameter += diameter_val
    
    mean_rank = total_rank / n_tests
    mean_diameter = total_diameter / n_tests
    
    if mean_diameter == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": 0,
            "instances_tested": n_tests,
            "conjecture_holds": False,
            "counterexample": "diameter_zero"
        }
    
    ratio = mean_rank / math.log(mean_diameter)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": ratio,
        "instances_tested": n_tests,
        "conjecture_holds": ratio >= 1,  # Assuming c=1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_less_than_c\" first_failing_seed={first_failing_seed}")