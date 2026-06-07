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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[rank], A[max_row] = A[max_row], A[rank]
            if A[rank][i] == 0:
                continue
            for j in range(m):
                if j != rank:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def generate_lattice(n):
        return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    def generate_xor_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['XOR', 'NOT'])
            if gate == 'XOR':
                inputs = [random.randint(0, 1) for _ in range(2)]
                circuit.append((gate, inputs))
            else:
                input_ = random.randint(0, 1)
                circuit.append((gate, input_))
        return circuit
    
    def entanglement_complexity(circuit):
        complexity = 0
        for gate, inputs in circuit:
            if gate == 'XOR':
                complexity += len(inputs) - 1
            else:
                complexity += 1
        return complexity
    
    def orbit_diameter(lattice):
        m, n = len(lattice), len(lattice[0])
        distances = [[math.inf] * n for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if lattice[i][j] == 1:
                    distances[i][j] = 0
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
        return max(max(row) for row in distances)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            lattice = generate_lattice(n)
            circuit = generate_xor_circuit(n)
            orbit_diam = orbit_diameter(lattice)
            entang_complexity_val = entanglement_complexity(circuit)
            results.append((orbit_diam, entang_complexity_val))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    x, y = zip(*results)
    r = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": r >= 0.8,
        "counterexample": "" if r >= 0.8 else f"r = {r}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 89))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")