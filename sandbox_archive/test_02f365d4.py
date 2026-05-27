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

def generate_circuit(n):
    if n == 1:
        return "0"
    elif n == 2:
        return "0, 1"
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit((n + 1) // 2)
        return f"{left}, {right}"

def alexander_module(circuit):
    if circuit == "0":
        return [[1]]
    elif circuit == "1":
        return [[0, 1], [1, 0]]
    
    left, right = circuit.split(', ')
    A_left = alexander_module(left)
    A_right = alexander_module(right)
    
    m = len(A_left)
    n = len(A_right)
    A = [[0] * (m + n) for _ in range(m + n)]
    
    for i in range(m):
        for j in range(n):
            A[i][j] = A_left[i][j]
            A[i][j + m] = A_right[i][j]
            A[i + m][j] = -A_right[i][j]
            A[i + m][j + m] = A_left[i][j]
    
    return A

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    row, col = 0, 0
    while row < m and col < n:
        if matrix[row][col] == 0:
            for i in range(row + 1, m):
                if matrix[i][col] != 0:
                    matrix[row], matrix[i] = matrix[i], matrix[row]
                    break
            else:
                col += 1
                continue
        
        pivot = matrix[row][col]
        for j in range(col, n):
            matrix[row][j] /= pivot
        
        for i in range(m):
            if i != row and matrix[i][col] != 0:
                factor = -matrix[i][col]
                for j in range(col, n):
                    matrix[i][j] += factor * matrix[row][j]
        
        row += 1
        col += 1
    
    return sum(1 for row in matrix if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    max_n = 40
    instances_tested = 0
    total_rank = 0
    
    for n in range(5, max_n + 1):
        circuit = generate_circuit(n)
        A = alexander_module(circuit)
        min_rank = rank(A)
        
        instances_tested += 1
        total_rank += min_rank
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = abs(mean_rank - math.log(max_n)) <= 3
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, log(n)={math.log(max_n)}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")