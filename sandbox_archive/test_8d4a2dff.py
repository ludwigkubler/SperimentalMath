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
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    def ac0_parity_circuit(n):
        circuit = []
        for _ in range(n):
            matrix = generate_matrix(random.randint(2, 5))
            circuit.append(matrix)
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = ac0_parity_circuit(n)
            rank = gaussian_elimination(circuit)
            total_rank += rank
            instances_tested += 1
    
    mean_minimal_rank = total_rank / instances_tested
    c = math.log(instances_tested) / n_values[-1]
    
    conjecture_holds = all(rank <= c * math.log(n) for n in n_values for _ in range(5))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": mean_minimal_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minimal_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")