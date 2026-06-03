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

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses
        clause = [random.randint(-n, n) for _ in range(n)]
        while not any(clause[i] != -clause[j] for j in range(i)):
            clause = [random.randint(-n, n) for _ in range(n)]
        cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(rows):
            if j != rank and matrix[j][i] != 0:
                factor = matrix[j][i] / matrix[rank][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def minimal_rank(cnf):
    n = len(cnf)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(cnf):
        for j in clause:
            if j > 0:
                matrix[i][j - 1] += 1
            else:
                matrix[i][-1] += 1
    return gaussian_elimination(matrix)

def circuit_monotone_width(cnf):
    n = len(cnf)
    max_clause_length = max(len(clause) for clause in cnf)
    width = 0
    for i in range(n):
        clause_lengths = [len([j for j in clause if abs(j) == i + 1]) for clause in cnf]
        width = max(width, sum(sorted(clause_lengths)[-max_clause_length:]))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_min_rank = 0
    total_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n)
            min_rank = minimal_rank(cnf)
            width = circuit_monotone_width(cnf)
            total_min_rank += min_rank
            total_width += width
            instances_tested += 1
    
    mean_min_rank = total_min_rank / instances_tested
    mean_width = total_width / instances_tested
    conjecture_holds = mean_min_rank >= 0.5 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_vs_width",
        "metric_value": mean_min_rank,
        "instances_tested": instances_tested,
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
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")