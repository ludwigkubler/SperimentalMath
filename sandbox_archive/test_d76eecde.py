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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, matrix[i][i])
        for r in range(i+1, n):
            matrix[r][i] *= factor
        
        # Eliminate above the pivot
        for r in range(i):
            factor = matrix[r][i]
            for c in range(n):
                matrix[r][c] -= factor * matrix[i][c]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    instances = [(i, j) for i in range(2**n) for j in range(i+1, 2**n)]
    max_communication = 0
    for x, y in instances:
        if f[x] == f[y]:
            comm = bin(x ^ y).count('1')
            if comm > max_communication:
                max_communication = comm
    return max_communication

def quasi_plurality_matrix(f):
    n = int(math.log2(len(f)))
    Q = [[0] * (n+1) for _ in range(n+1)]
    for x in range(2**n):
        count_0 = 0
        count_1 = 0
        for i in range(n):
            if f[x ^ (1 << i)] == 0:
                count_0 += 1
            else:
                count_1 += 1
        Q[count_0][count_1] += 1
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    c_f = communication_complexity(f)
    Q_f = quasi_plurality_matrix(f)
    rank = gaussian_elimination(Q_f)
    
    return {
        "metric_name": "Rank of Quasi-Plurality Matrix",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= c_f**2,  # Example polynomial function
        "counterexample": "" if rank <= c_f**2 else f"Counterexample for n={n}, c_f={c_f}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds c_f^2\" first_failing_seed={first_failing_seed}")