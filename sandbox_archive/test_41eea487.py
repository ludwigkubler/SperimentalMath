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
    
    def generate_random_circuit(n: int):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        n = len(circuit) + 1
        width = [0] * (n + 1)
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                width[inputs[0]] += 1
                width[inputs[1]] += 1
                width[n - 1] -= 2
            elif gate == 'OR':
                width[inputs[0]] += 1
                width[inputs[1]] += 1
                width[n - 1] -= 1
        return max(width)
    
    def compute_noncommutative_rank(circuit):
        n = len(circuit) + 1
        rank = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                rank += 2
            elif gate == 'OR':
                rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_minimal_rank(circuit):
        n = len(circuit) + 1
        identity_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            identity_matrix[i][i] = 1
        
        augmented_matrix = [row[:] + [1] for row in circuit]
        augmented_matrix.extend(identity_matrix)
        
        rank = gaussian_elimination(augmented_matrix)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        monotone_width = compute_monotone_width(circuit)
        minimal_rank = compute_minimal_rank(circuit)
        
        if monotone_width == 0:
            continue
        
        results.append({
            "n": n,
            "monotone_width": monotone_width,
            "minimal_rank": minimal_rank
        })
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["minimal_rank"] for result in results]
    support_fraction = sum(1 for value in metric_values if abs(value - result["monotone_width"]) <= 3) / len(metric_values)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    support_fraction = sum(1 for value in metric_values if abs(value - result["monotone_width"]) <= 3) / len(metric_values)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")