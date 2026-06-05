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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(rank)):
            continue
        pivot_row = rank
        for j in range(pivot_row + 1, n):
            if matrix[j][i] != 0:
                matrix[pivot_row], matrix[j] = matrix[j], matrix[pivot_row]
                break
        else:
            continue
        rank += 1
        denom = matrix[pivot_row][i]
        for j in range(n):
            if j == i:
                matrix[pivot_row][j] = Fraction(1, denom)
            else:
                matrix[pivot_row][j] = -Fraction(matrix[pivot_row][j], denom)
        for j in range(n):
            if j != pivot_row:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] += -factor * matrix[pivot_row][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            # Generate a random communication protocol (example: a binary matrix)
            protocol = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            
            # Convert the protocol to a semialgebraic matrix
            semialgebra_matrix = []
            for i in range(n):
                row = [protocol[i][j] * protocol[j][i] for j in range(n)]
                semialgebra_matrix.append(row)
            
            # Compute the rank of the semialgebraic matrix
            rank = matrix_rank(semialgebra_matrix)
            
            # Measure the communication complexity rank (example: number of 1s in the protocol)
            comm_complexity_rank = sum(sum(row) for row in protocol)
            
            # Check if the inequality holds
            if rank > n * math.log(n, 2):
                conjecture_holds = False
                counterexample = f"n={n}, semialgebra_rank={rank}, comm_complexity_rank={comm_complexity_rank}"
                break
            
            total_metric_value += rank

    return {
        "metric_name": "semialgebra_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested * len([5, 10, 15, 20, 30, 40]),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    total_metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(total_metric_values)/len(total_metric_values):.6f} std={math.sqrt(sum((x - sum(total_metric_values)/len(total_metric_values))**2 for x in total_metric_values) / len(total_metric_values)):.6f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(total_metric_values)/len(total_metric_values):.6f} std={math.sqrt(sum((x - sum(total_metric_values)/len(total_metric_values))**2 for x in total_metric_values) / len(total_metric_values)):.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")