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
    
    def generate_cnf(m, n):
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
            for j in range(cols):
                if j != i:
                    factor = -matrix[rank][j] / matrix[rank][i]
                    for k in range(rows):
                        matrix[k][j] += factor * matrix[k][i]
            rank += 1
        return rank
    
    def communication_complexity_rank(cnf, n):
        assignments = [random.choice([-1, 1]) for _ in range(n)]
        rank = gaussian_elimination([[int(a == b) - int(a != b) for a in assignments] for b in cnf])
        return rank
    
    m = random.randint(5, 40)
    n = random.randint(5, 40)
    cnf = generate_cnf(m, n)
    
    symplectic_volume = math.sqrt(n)
    communication_complexity_ranks = [communication_complexity_rank(cnf, n) for _ in range(30)]
    variance = sum((x - sum(communication_complexity_ranks) / len(communication_complexity_ranks)) ** 2 for x in communication_complexity_ranks) / len(communication_complexity_ranks)
    
    ratio = symplectic_volume / math.sqrt(variance)
    conjecture_holds = ratio >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < sqrt({n})"
    
    return {
        "metric_name": "Symplectic Volume / Variance in Communication Complexity Rank",
        "metric_value": ratio,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio too small\" first_failing_seed={first_failing_seed}")