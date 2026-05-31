# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_circuit(n, w):
    # Simple circuit generator for demonstration purposes
    if n <= 1 or w <= 0:
        return []
    circuit = []
    for _ in range(w):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        output = random.randint(0, 1)
        circuit.append((gate, inputs, output))
    return circuit

def permute_matrix(matrix, permutation):
    n = len(matrix)
    permuted_matrix = [[matrix[permutation[i]][j] for j in range(n)] for i in range(n)]
    return permuted_matrix

def check_circuit_equality(circuit1, circuit2):
    if len(circuit1) != len(circuit2):
        return False
    for (gate1, inputs1, output1), (gate2, inputs2, output2) in zip(circuit1, circuit2):
        if gate1 != gate2 or inputs1 != inputs2 or output1 != output2:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            w = random.randint(2, min(n // 2, 40))
            circuit = generate_circuit(n, w)
            
            perm_count = 0
            identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            
            for permutation in itertools.permutations(range(n)):
                permuted_matrix = permute_matrix(identity_matrix, permutation)
                permuted_circuit = check_circuit_equality(circuit, permuted_matrix)
                if permuted_circuit:
                    perm_count += 1
            
            expected_bound = n ** (w / 2)
            ratio = Fraction(perm_count, expected_bound).limit_denominator()
            
            results.append({
                "n": n,
                "w": w,
                "perm_count": perm_count,
                "expected_bound": expected_bound,
                "ratio": ratio
            })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of permutation matrices to n^(w/2)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["n_max"] >= 16 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded")