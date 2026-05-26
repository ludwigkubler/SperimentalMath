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

def generate_xor_and_tree(n):
    if n == 1:
        return 'x1'
    else:
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return f'({left} & {right}) | ({left} ^ {right})'

def ac0_circuit_to_polynomial(circuit):
    if circuit == 'x1':
        return 'x1'
    elif circuit.startswith('(') and circuit.endswith(')'):
        left, op, right = circuit[1:-1].split()
        if op == '&':
            return f'({ac0_circuit_to_polynomial(left)} & {ac0_circuit_to_polynomial(right)})'
        elif op == '^':
            return f'({ac0_circuit_to_polynomial(left)} ^ {ac0_circuit_to_polynomial(right)})'
    else:
        raise ValueError("Invalid circuit format")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    if n < 5 or n > 40:
        return {
            "metric_name": "degree",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "invalid_n"
        }
    
    degree_sum = 0
    instances_tested = 0
    
    for _ in range(30):
        circuit = generate_xor_and_tree(n)
        polynomial = ac0_circuit_to_polynomial(circuit)
        
        # Count the number of XOR and AND operations
        xor_count = polynomial.count('^')
        and_count = polynomial.count('&')
        
        # The degree is the maximum of XOR and AND counts
        degree = max(xor_count, and_count)
        
        if degree < math.log(n):
            return {
                "metric_name": "degree",
                "metric_value": -1,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": f"seed={seed}, n={n}, degree={degree}, expected=Ω(log {n})"
            }
        
        degree_sum += degree
        instances_tested += 1
    
    mean_degree = degree_sum / instances_tested
    return {
        "metric_name": "degree",
        "metric_value": mean_degree,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_degree >= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_degree = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_degree} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='degree < Ω(log n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")