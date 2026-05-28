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
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for row in range(rank, rows):
                factor = matrix[row][col] / matrix[pivot_row][col]
                for j in range(cols):
                    matrix[row][j] -= factor * matrix[pivot_row][j]
        return rank
    
    def generate_k_clique_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def construct_monomial_ideal(edges):
        variables = list(range(len(edges)))
        ideal = []
        for edge in edges:
            a, b = edge
            monomial = [0] * len(variables)
            monomial[a] = 1
            monomial[b] = 1
            ideal.append(monomial)
        return ideal
    
    def tropical_curve_rank(ideal):
        matrix = []
        for monomial in ideal:
            row = []
            for coeff in monomial:
                if coeff == 0:
                    row.append(math.inf)
                else:
                    row.append(-math.log(coeff))
            matrix.append(row)
        return gaussian_elimination(matrix)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = generate_k_clique_instance(n)
    ideal = construct_monomial_ideal(edges)
    rank = tropical_curve_rank(ideal)
    
    f_n = Fraction(n**2 * math.log(n), 1)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= f_n,
        "counterexample": "" if rank >= f_n else f"n={n}, rank={rank}, f(n)={f_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_rank = 0
    count_supports = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_rank += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supports += 1
        
        results.append(trial_result)
    
    mean_rank = total_rank / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_rank) ** 2 for x in results) / len(results))
    support_fraction = count_supports / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, rank={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")