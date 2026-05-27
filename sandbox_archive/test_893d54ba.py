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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def generate_random_circuit(n):
    circuit = []
    for _ in range(n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for gate_type, inputs in reversed(circuit):
        if gate_type == 'AND':
            result = all(inputs)
        elif gate_type == 'OR':
            result = any(inputs)
        stack.append(result)
    return stack.pop()

def find_minimal_order(p_adic_units):
    p_adic_units = sorted(p_adic_units)
    for i in range(1, len(p_adic_units) + 1):
        if all(p_adic_units[j] % p_adic_units[i] == 0 for j in range(i)):
            return i
    return len(p_adic_units)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    p_adic_units = [random.randint(2, 100) for _ in range(10)]
    
    try:
        result = evaluate_circuit(circuit)
        o_S = find_minimal_order(p_adic_units)
        sqrt_n = math.sqrt(n)
        
        if o_S <= sqrt_n:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "o(S) > √n"
    except Exception as e:
        return {
            "metric_name": "conjecture_holds",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "metric_name": "o(S)",
        "metric_value": o_S,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"o(S) > √n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")