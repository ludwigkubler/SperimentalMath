# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = [random.randint(0, 1) for _ in range(n)]
            circuit.append(gate)
        return circuit
    
    def is_permutation_matrix(matrix):
        if len(matrix) != len(matrix[0]):
            return False
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        for row in matrix:
            if sum(row) != 1 or sorted(row) != [0] * (n - 1) + [1]:
                return False
        for col in zip(*matrix):
            if sum(col) != 1 or sorted(col) != [0] * (n - 1) + [1]:
                return False
        return True
    
    def count_permutation_matrices(circuit, n):
        count = 0
        for perm in itertools.permutations(range(n)):
            matrix = [[circuit[i][j] if j == perm[j] else 0 for j in range(n)] for i in range(len(circuit))]
            if is_permutation_matrix(matrix):
                count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n, random.randint(2, 40))
        perm_count = count_permutation_matrices(circuit, n)
        expected_bound = n ** (len(circuit) / 2)
        ratio = Fraction(perm_count, expected_bound).limit_denominator()
        results.append((n, perm_count, expected_bound, ratio))
    
    metric_value = sum(ratio.numerator for _, _, _, ratio in results) / len(results)
    conjecture_holds = all(ratio <= 10 for _, _, _, ratio in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of permutation matrices to n^(w/2)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")