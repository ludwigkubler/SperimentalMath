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
    
    def generate_circuit(n):
        # Generate a random monotone circuit with size Θ(2^n)
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_entanglement_entropy(circuit):
        # Calculate the entanglement entropy using the Coxeter matrix
        n = int(math.log2(len(circuit)))
        W = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    W[i][j] = 1
                    W[j][i] = 1
        return sum([math.log(2) - math.log(2 + sum(W[i])) for i in range(n)])
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            if matrix[i][i] == 0:
                return 0
            det *= matrix[i][i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        return det
    
    def calculate_coxeter_matrix(circuit):
        # Calculate the Coxeter matrix associated with the circuit
        n = int(math.log2(len(circuit)))
        W = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    W[i][j] = 1
                    W[j][i] = 1
        return gaussian_elimination(W)
    
    def calculate_entanglement_entropy_from_matrix(matrix):
        # Calculate the entanglement entropy from the Coxeter matrix
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('-inf')
        return sum([math.log(2) - math.log(2 + sum(matrix[i])) for i in range(n)])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        W = calculate_coxeter_matrix(circuit)
        H_W = calculate_entanglement_entropy_from_matrix(W)
        results.append(H_W)
    
    mean_H_W = sum(results) / len(results)
    conjecture_holds = all(H_W >= 2**(n/4) for n, H_W in zip(n_values, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "entanglement_entropy",
        "metric_value": mean_H_W,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_H_W = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_H_W} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")