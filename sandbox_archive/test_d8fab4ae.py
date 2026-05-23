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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if matrix[i][i] != 0:
                rank += 1
        return rank

    def generate_parity_circuit(n):
        circuit = []
        for _ in range(2**(n-1)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.choice([0, 1]) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit

    def tropicalize_circuit(circuit):
        n = len(circuit[0][1])
        p_adic_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in range(n):
                    if inputs[i] == 1:
                        p_adic_matrix[0][i+1] += 1
            elif gate == 'OR':
                for i in range(n):
                    if inputs[i] == 0:
                        p_adic_matrix[0][i+1] += 1
        return p_adic_matrix

    def compute_minimal_rank(p_adic_matrix):
        rank_value = rank(gaussian_elimination(p_adic_matrix))
        return rank_value

    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_parity_circuit(n)
    p_adic_matrix = tropicalize_circuit(circuit)
    minimal_rank = compute_minimal_rank(p_adic_matrix)

    instances_tested = 1
    conjecture_holds = minimal_rank == math.log2(n + 1)
    counterexample = "" if conjecture_holds else "minimal_rank does not match log(n)"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank does not match log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")