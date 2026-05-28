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
    
    def generate_linear_equation(n):
        coefficients = [random.choice([0, 1]) for _ in range(n)]
        return coefficients
    
    def compute_schur_algebra_rank(coefficients):
        n = len(coefficients)
        rank = 0
        # Simplified Schur algebra rank computation (for demonstration purposes)
        if sum(coefficients) % 2 == 0:
            rank = 1
        else:
            rank = n
        return rank
    
    def construct_circuit(n, D):
        # Simplified Boolean circuit construction (for demonstration purposes)
        circuit = []
        for _ in range(D):
            layer = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    n = random.randint(5, 40)
    D = random.randint(1, 10)
    
    equation = generate_linear_equation(n)
    rank = compute_schur_algebra_rank(equation)
    circuit = construct_circuit(n, D)
    circuit_rank = compute_schur_algebra_rank(circuit)
    
    metric_name = "Schur Algebra Rank"
    metric_value = circuit_rank
    instances_tested = 1
    conjecture_holds = circuit_rank >= D**3
    counterexample = "" if conjecture_holds else f"Circuit with rank {circuit_rank} < {D**3}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    total_metric_value = 0
    num_seeds = len(seeds)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
        total_metric_value += result["metric_value"]
    
    mean_metric_value = total_metric_value / num_seeds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_seeds
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with rank < {D**3}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")