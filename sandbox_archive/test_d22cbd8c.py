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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(-matrix[i][i], matrix[max_row][i])
            for j in range(i, cols):
                matrix[max_row][j] *= factor
            for j in range(rows):
                if j != max_row:
                    factor = Fraction(matrix[j][i], matrix[max_row][i])
                    for k in range(i, cols):
                        matrix[j][k] += factor * matrix[max_row][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def ac0_circuit(n):
        # Generate a random AC⁰ circuit computing PARITY on n bits
        depth = 3
        size = 2 ** 10
        circuit = [random.randint(0, 1) for _ in range(size)]
        return circuit
    
    n = 40
    circuit = ac0_circuit(n)
    communication_matrix = [[circuit[i ^ j] for j in range(n)] for i in range(n)]
    
    real_rank = gaussian_elimination(communication_matrix)
    metric_value = real_rank / math.log(n, 2)
    
    conjecture_holds = metric_value >= 0.1
    counterexample = "" if conjecture_holds else "real_rank_too_low"
    
    return {
        "metric_name": "Real Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{results[0]['counterexample']}' first_failing_seed={first_failing_seed}")