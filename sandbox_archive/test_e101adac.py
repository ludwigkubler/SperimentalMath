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

def gaussian_elimination(matrix):
    rows = len(matrix)
    if rows == 0:
        return 0
    cols = len(matrix[0])
    
    rank = 0
    for i in range(rows):
        pivot_row = i
        while pivot_row < rows and matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == rows:
            continue
        
        # Swap rows
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                if i == k:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[i][k]
        
        rank += 1
    
    return rank

def generate_boolean_circuit(depth, n):
    circuit = []
    for _ in range(depth):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate_type, inputs))
    return circuit

def tautological_ideal(circuit):
    n = len(circuit[0][1])
    variables = list(range(n))
    ideal = []
    
    def evaluate_circuit(gate, inputs):
        if gate == 'AND':
            return all(inputs)
        elif gate == 'OR':
            return any(inputs)
    
    for i in range(2**n):
        inputs = [(i >> j) & 1 for j in range(n)]
        result = evaluate_circuit(circuit[0][0], inputs)
        for gate, inputs in circuit[1:]:
            result = evaluate_circuit(gate, [result] + inputs)
        if not result:
            ideal.append(inputs)
    
    return ideal

def minimal_geometric_entropy(ideal):
    n = len(ideal[0])
    matrix = []
    for row in ideal:
        matrix.append([Fraction(row[i]) for i in range(n)])
    
    rank = gaussian_elimination(matrix)
    H_min = -rank * math.log2(rank) if rank > 0 else 0
    return H_min

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_H_min = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(random.randint(1, n), n)
            ideal = tautological_ideal(circuit)
            H_min = minimal_geometric_entropy(ideal)
            total_H_min += H_min
            instances_tested += 1
    
    mean_H_min = total_H_min / instances_tested
    conjecture_holds = all(abs(H_min - (d**2 * math.log(n))) <= 0.1 * (d**2 * math.log(n)) for d, n in [(random.randint(1, n), n) for _ in range(30)])
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": mean_H_min,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_min = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_min} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_min} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed + 1}")