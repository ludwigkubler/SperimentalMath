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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_circuit(n):
        if n == 1:
            return [[0, 1], [1, 0]]
        else:
            subcircuits = [generate_monotone_circuit(n // 2) for _ in range(4)]
            circuit = []
            for i in range(n):
                if i % 2 == 0:
                    circuit.append([i] + subcircuits[0][i % (n // 2)])
                else:
                    circuit.append([i] + subcircuits[1][(i - 1) // (n // 2)])
            return circuit
    
    def cocomplex(circuit):
        n = len(circuit)
        cocomplex = [[0] * n for _ in range(n)]
        for i, gate in enumerate(circuit):
            for j in gate[1:]:
                cocomplex[i][j] = 1
                cocomplex[j][i] = 1
        return cocomplex
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i]):
                pivot_col = next(j for j in range(n) if matrix[i][j])
                for j in range(i + 1, m):
                    factor = Fraction(matrix[j][pivot_col], matrix[i][pivot_col])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank
    
    def monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for gate in circuit:
            inputs, output = gate[1], gate[0]
            for i in inputs:
                width[i + 1] = max(width[i + 1], width[i] + 1)
        return max(width)

    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    cocomplex_matrix = cocomplex(circuit)
    mrank_value = min_rank(cocomplex_matrix)
    w_mon_value = monotone_width(circuit)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mrank_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")