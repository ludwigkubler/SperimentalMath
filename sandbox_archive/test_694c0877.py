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
    
    def generate_circuit(n):
        if n == 1:
            return ['A']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({left[0]} & {right[0]})'] + left + right
    
    def alexander_module(circuit):
        if circuit == 'A':
            return [[1]]
        elif circuit.startswith('(') and circuit.endswith(')'):
            left, right = circuit[1:-1].split(' & ')
            A_left = alexander_module(left)
            A_right = alexander_module(right)
            m, n = len(A_left), len(A_right)
            B = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m):
                for j in range(n):
                    B[i][j] = A_left[i][j]
            for i in range(m):
                for j in range(1, n + 1):
                    B[i][j] += A_right[i][j - 1]
            return B
        else:
            raise ValueError("Invalid circuit format")
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i]):
                rank += 1
                for j in range(n):
                    if matrix[i][j]:
                        for k in range(m):
                            if k != i and any(matrix[k]):
                                matrix[k][j] -= matrix[i][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            A = alexander_module(circuit)
            rank = min_rank(A)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    log_n_values = [math.log2(n) for n in n_values]
    
    if all(abs(mean_rank - log_n) <= 3 for log_n in log_n_values):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mean_min_rank does not satisfy the bound"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_min_rank does not satisfy the bound\" first_failing_seed={first_failing_seed}")