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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(1, A[i][i])
        for k in range(i+1, n):
            A[k][i] *= factor
        
        # Eliminate above
        for k in range(i):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    
    rank = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(n)):
            continue
        rank += 1
    
    return rank

def generate_ac0_circuit(n, d):
    # Generate a random AC^0 circuit of depth d computing parity on n bits
    # This is a simplified model and does not represent real AC^0 circuits
    if d == 1:
        return [[i % 2 for i in range(n)]]
    else:
        layers = generate_ac0_circuit(n, d-1)
        new_layer = []
        for i in range(n):
            new_layer.append([layers[j][i] ^ layers[(j+1) % n][i] for j in range(len(layers))])
        return [new_layer]

def communication_matrix(circuit):
    n = len(circuit[0])
    m = len(circuit)
    comm_matrix = [[0] * (n * m) for _ in range(n * m)]
    
    for i in range(n):
        for j in range(m):
            for k in range(n):
                if circuit[j][k] == i % 2:
                    comm_matrix[i * n + k][j * n + k] = 1
    
    return comm_matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        d = 1
        circuit = generate_ac0_circuit(n, d)
        comm_matrix = communication_matrix(circuit)
        
        real_rank = gaussian_elimination(comm_matrix)
        expected_rank = math.ceil(n ** (1 / (d - 1)))
        
        results.append({
            "n": n,
            "real_rank": real_rank,
            "expected_rank": expected_rank
        })
    
    metric_value = sum(result["real_rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["real_rank"] >= result["expected_rank"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Real Rank",
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
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")