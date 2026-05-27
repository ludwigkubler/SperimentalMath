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

def generate_tseitin_circuit(n, D):
    if n <= 0 or D <= 0:
        raise ValueError("n and D must be positive integers")
    
    # Generate a random Tseitin circuit of size S and depth D
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Base case: generate literals
    for var in variables:
        clauses.append([var])
    
    # Recursive case: generate clauses based on depth
    def generate_clauses(depth):
        if depth == 1:
            return
        new_clauses = []
        for i in range(len(clauses)):
            clause = clauses[i]
            if len(clause) > 1:
                new_var = f'x{len(variables)+i+1}'
                variables.append(new_var)
                new_clauses.extend([[new_var, clause[0], clause[1]], [new_var, '!', clause[0]], [new_var, '!', clause[1]]])
        clauses.extend(new_clauses)
        generate_clauses(depth - 1)
    
    generate_clauses(D)
    
    # Convert to Tseitin circuit
    tseitin_circuit = []
    for i, clause in enumerate(clauses):
        if len(clause) == 1:
            tseitin_circuit.append([clause[0]])
        else:
            new_var = f'y{i+1}'
            variables.append(new_var)
            tseitin_circuit.append([new_var, clause[0], clause[1]])
            tseitin_circuit.append([new_var, '!', clause[2]])
    
    return tseitin_circuit

def generate_qmc_sequence(n, D):
    if n <= 0 or D <= 0:
        raise ValueError("n and D must be positive integers")
    
    # Generate a quasi-Monte Carlo sequence of degree D
    qmc_sequence = []
    for i in range(2**D):
        point = [math.cos(2 * math.pi * (i // (2**(j+1))) / 2**j) for j in range(D)]
        qmc_sequence.append(point)
    
    return qmc_sequence

def compute_min_distance(qmc_sequence):
    if not qmc_sequence:
        raise ValueError("QMC sequence must not be empty")
    
    min_dist = float('inf')
    n = len(qmc_sequence[0])
    
    for i in range(len(qmc_sequence)):
        for j in range(i + 1, len(qmc_sequence)):
            dist = sum((qmc_sequence[i][k] - qmc_sequence[j][k]) ** 2 for k in range(n))
            if dist < min_dist:
                min_dist = dist
    
    return math.sqrt(min_dist)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    D = random.randint(1, 10)
    
    try:
        circuit = generate_tseitin_circuit(n, D)
        qmc_sequence = generate_qmc_sequence(n, D)
        min_dist = compute_min_distance(qmc_sequence)
        
        metric_value = min_dist
        instances_tested = 1
        conjecture_holds = False
        counterexample = ""
        
        return {
            "metric_name": "min_dist",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    except Exception as e:
        return {
            "metric_name": "min_dist",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*2 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")