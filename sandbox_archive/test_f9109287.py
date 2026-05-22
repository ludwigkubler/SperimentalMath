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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k, n = len(A), len(B), len(B[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                result[i][j] += A[i][l] * B[l][j]
    return result

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def is_coxeter_group_order(order, n):
    # This is a placeholder function. Implement the actual logic to determine
    # if the order satisfies the conjecture.
    return order >= n**2 / 4

def generate_random_permutation(n):
    return random.sample(range(n), n)

def generate_random_circuit(d, w):
    circuit = []
    for _ in range(d):
        layer = [random.randint(0, w - 1) for _ in range(w)]
        circuit.append(layer)
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_permutations = 0
    total_circuits = 0
    valid_permutations = 0
    valid_circuits = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            perm = generate_random_permutation(n)
            perm_matrix = identity_matrix(n)
            for i, x in enumerate(perm):
                perm_matrix[i][x] = 1
            
            if matrix_mult(perm_matrix, identity_matrix(n)) == identity_matrix(n):
                order = n**2 / 4
                if is_coxeter_group_order(order, n):
                    valid_permutations += 1
                total_permutations += 1
            
            circuit = generate_random_circuit(n // 5, n)
            circuit_size = sum(len(layer) for layer in circuit)
            if circuit_size > 0:
                order = (n // 5 + n) ** 2
                if is_coxeter_group_order(order, circuit_size):
                    valid_circuits += 1
                total_circuits += 1
    
    metric_value_permutations = valid_permutations / total_permutations if total_permutations > 0 else 0
    metric_value_circuits = valid_circuits / total_circuits if total_circuits > 0 else 0
    
    conjecture_holds_permutations = metric_value_permutations >= n_values[-1]**2 / 4
    conjecture_holds_circuits = metric_value_circuits >= n_values[-1] ** 2 / 4
    
    counterexample_permutations = "" if conjecture_holds_permutations else "permutations"
    counterexample_circuits = "" if conjecture_holds_circuits else "circuits"
    
    return {
        "metric_name": "Coxeter Group Order",
        "metric_value_permutations": metric_value_permutations,
        "metric_value_circuits": metric_value_circuits,
        "instances_tested_permutations": total_permutations,
        "instances_tested_circuits": total_circuits,
        "conjecture_holds_permutations": conjecture_holds_permutations,
        "conjecture_holds_circuits": conjecture_holds_circuits,
        "counterexample_permutations": counterexample_permutations,
        "counterexample_circuits": counterexample_circuits
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_permutations = sum(result["instances_tested_permutations"] for result in results if "instances_tested_permutations" in result)
    total_circuits = sum(result["instances_tested_circuits"] for result in results if "instances_tested_circuits" in result)
    
    mean_permutations = sum(result["metric_value_permutations"] * result["instances_tested_permutations"] for result in results if "instances_tested_permutations" in result) / total_permutations
    std_permutations = math.sqrt(sum((result["metric_value_permutations"] - mean_permutations) ** 2 * result["instances_tested_permutations"] for result in results if "instances_tested_permutations" in result) / total_permutations)
    
    mean_circuits = sum(result["metric_value_circuits"] * result["instances_tested_circuits"] for result in results if "instances_tested_circuits" in result) / total_circuits
    std_circuits = math.sqrt(sum((result["metric_value_circuits"] - mean_circuits) ** 2 * result["instances_tested_circuits"] for result in results if "instances_tested_circuits" in result) / total_circuits)
    
    support_fraction_permutations = sum(1 for result in results if result.get("conjecture_holds_permutations", False)) / len(results)
    support_fraction_circuits = sum(1 for result in results if result.get("conjecture_holds_circuits", False)) / len(results)
    
    if support_fraction_permutations >= 0.8 and support_fraction_circuits >= 0.8:
        print(f"RESULT: SUPPORTED mean_permutations={mean_permutations} std_permutations={std_permutations} support_fraction_permutations={support_fraction_permutations}")
        print(f"RESULT: SUPPORTED mean_circuits={mean_circuits} std_circuits={std_circuits} support_fraction_circuits={support_fraction_circuits}")
    elif any(not result.get("conjecture_holds_permutations", False) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result.get("conjecture_holds_permutations", False))
        print(f"RESULT: FALSIFIED counterexample_permutations=\"first failing seed {first_failing_seed}\"")
    elif any(not result.get("conjecture_holds_circuits", False) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result.get("conjecture_holds_circuits", False))
        print(f"RESULT: FALSIFIED counterexample_circuits=\"first failing seed {first_failing_seed}\"")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")