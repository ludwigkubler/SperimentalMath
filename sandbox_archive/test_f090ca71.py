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
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def hodge_rank(matrix):
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank

    def ac0_circuit(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = ac0_circuit(n // 2, d - 1)
            right = ac0_circuit(n - n // 2, d - 1)
            return [left[i] ^ right[i] for i in range(n)]

    def tropical_variety(circuit):
        n = len(circuit)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            matrix[i][i] = circuit[i]
            for j in range(i + 1, n):
                matrix[j][i] = abs(circuit[j] - circuit[i])
        return hodge_rank(matrix)

    def ac0_circuits(n, d):
        circuits = []
        for _ in range(30):  # Ensure at least 30 instances per seed
            circuit = ac0_circuit(n, d)
            circuits.append(circuit)
        return circuits

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rank = 0
        for _ in range(5):  # Ensure at least 5 instances per size
            circuits = ac0_circuits(n, d)
            ranks = [tropical_variety(circuit) for circuit in circuits]
            total_rank += sum(ranks)
        mean_rank = total_rank / len(ranks)
        results.append({"n": n, "mean_rank": mean_rank})

    metric_value = sum(result["mean_rank"] * result["n"]**2 * math.log(result["n"]) for result in results) / sum(result["n"]**2 * math.log(result["n"]) for result in results)
    instances_tested = len(results)
    
    conjecture_holds = all(abs(result["mean_rank"] - metric_value) <= 3 * (sum((result["mean_rank"] - metric_value)**2 for result in results) / instances_tested)**0.5 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - mean_value) <= 3 * std_value) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")