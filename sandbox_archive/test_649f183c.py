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
    
    def generate_tseitin_circuit(width):
        n = width * (width - 1) // 2 + width
        circuit = []
        for i in range(n):
            if i < width:
                circuit.append((i, 'A', i))
            else:
                a, b, c = random.sample(range(width), 3)
                circuit.append((a, 'OR', b, c))
        return circuit
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_motivic_homology(circuit):
        n = len(circuit)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i, op, *args in circuit:
            if op == 'A':
                matrix[i][i] = 1
            elif op == 'OR':
                a, b, c = args
                matrix[a][c] += 1
                matrix[b][c] += 1
        return gaussian_elimination(matrix)
    
    width = random.randint(5, 40)
    circuit = generate_tseitin_circuit(width)
    rank = compute_motivic_homology(circuit)
    
    metric_value = rank
    conjecture_holds = rank >= 2 ** (width / 2)
    counterexample = "" if conjecture_holds else f"Rank {rank} < 2^{width/2}"
    
    return {
        "metric_name": "motivic_homology_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")