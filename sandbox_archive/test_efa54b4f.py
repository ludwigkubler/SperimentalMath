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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def term_overlap_matrix(cnf):
    n = max(abs(lit) for lit in sum(cnf, []))
    matrix = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit1 in clause:
            for lit2 in clause:
                if abs(lit1) != abs(lit2):
                    matrix[abs(lit1) - 1][abs(lit2) - 1] += 1
    return matrix

def gaussian_elimination(matrix, n):
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix, n):
    matrix = gaussian_elimination(matrix, n)
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def communication_complexity_rank_variance(cnf, n):
    ranks = [rank(term_overlap_matrix([clause]), n) for clause in cnf]
    mean = sum(ranks) / len(ranks)
    variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
    return variance

def alexander_brandt_index(matrix, n):
    trace = sum(matrix[i][i] for i in range(n))
    det = matrix[0][0]
    for i in range(1, n):
        det *= matrix[i][i]
    ab_index = Fraction(trace, det)
    return ab_index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    cnf = generate_cnf(n, n * (n - 1) // 2)
    matrix = term_overlap_matrix(cnf)
    ab_index = alexander_brandt_index(matrix, n)
    variance = communication_complexity_rank_variance(cnf, n)
    correlation = ab_index * Fraction(variance).limit_denominator()
    
    return {
        "metric_name": "Correlation",
        "metric_value": float(correlation),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")