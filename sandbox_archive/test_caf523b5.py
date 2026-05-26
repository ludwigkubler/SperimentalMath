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
        return "x1"
    else:
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return f"({left} & {right}) | ({left} ^ {right})"

def ac0_circuit_to_polynomial(circuit):
    if circuit.startswith("x"):
        return circuit
    left, op, right = circuit[1:-1].split()
    if op == "&":
        return f"{ac0_circuit_to_polynomial(left)} * {ac0_circuit_to_polynomial(right)}"
    elif op == "|":
        return f"({ac0_circuit_to_polynomial(left)}) + ({ac0_circuit_to_polynomial(right)})"
    elif op == "^":
        return f"({ac0_circuit_to_polynomial(left)}) - ({ac0_circuit_to_polynomial(right)})"
    else:
        raise ValueError("Invalid operation")

def degree_of_polynomial(poly):
    if poly.startswith("(") and poly.endswith(")"):
        return max(degree_of_polynomial(subpoly) for subpoly in poly[1:-1].split())
    elif "*" in poly or "+" in poly or "-" in poly:
        left, op, right = poly.split()
        return 1 + max(degree_of_polynomial(left), degree_of_polynomial(right))
    else:
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_xor_and_tree(n)
        polynomial = ac0_circuit_to_polynomial(circuit)
        degree = degree_of_polynomial(polynomial)
        
        results.append({
            "n": n,
            "circuit": circuit,
            "polynomial": polynomial,
            "degree": degree
        })
    
    avg_degree = sum(result["degree"] for result in results) / len(results)
    conjecture_holds = all(result["degree"] >= math.log(n, 2) for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, degree={results[0]['degree']}"
    
    return {
        "metric_name": "average_degree",
        "metric_value": avg_degree,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_degree = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_degree} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"degree<{math.log(results[0]['n'], 2)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")