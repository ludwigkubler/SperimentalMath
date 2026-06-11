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
        n = len(matrix)
        rank = 0
        for i in range(n):
            if rank >= n:
                break
            pivot_row = rank
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    pivot_row = rank
                    i += 1
                    if i == n:
                        return rank
            matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
            pivot = matrix[rank][i]
            for j in range(n):
                if j != i:
                    factor = Fraction(matrix[j][i], pivot)
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                row, col = abs(lit) - 1, lit > 0
                matrix[row][col] += 1
                matrix[col][row] += 1
        return gaussian_elimination(matrix)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 ** n):
            clause = set()
            for i in range(n):
                if random.choice([True, False]):
                    clause.add(i + 1)
                else:
                    clause.add(-(i + 1))
            cnf.append(list(clause))
        return cnf
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        rank_variance = communication_complexity_rank_variance(cnf)
        if rank_variance == 0:
            continue
        metric_values.append(abs(len(cnf) - rank_variance))
    
    if not metric_values:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.5 * mean <= val <= 2 * mean for val in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")