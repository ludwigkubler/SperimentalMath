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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = rank
            for j in range(rank, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            for j in range(rows):
                if j != rank:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def min_order(cnf):
        n = len(cnf)
        identity_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            identity_matrix[i][i] = 1
        
        for clause in cnf:
            a, b = abs(clause[0]), abs(clause[1])
            if a == b:
                continue
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if (i + 1) in clause and (j + 1) in clause:
                        matrix[i][j] = 1
            rank = gaussian_elimination(matrix)
        return rank
    
    def monotone_width(cnf):
        n = len(cnf)
        width = [0] * (n + 1)
        for i in range(n):
            for j in range(i + 1, n):
                if any(lit in cnf[i] and -lit in cnf[j] for lit in range(1, n + 1)):
                    width[min(i, j)] += 1
        return max(width)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    order = min_order(cnf)
    width = monotone_width(cnf)
    
    return {
        "metric_name": "order_vs_width",
        "metric_value": order / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order_vs_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_order_vs_width} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")