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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = 1 / matrix[i][i]
        for j in range(i, n):
            matrix[i][j] *= factor
        for k in range(i+1, n):
            factor = matrix[k][i]
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(m)):
            continue
        rank += 1
        factor = 1 / matrix[i][i]
        for j in range(i, m):
            matrix[i][j] *= factor
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, m):
                    matrix[k][j] -= factor * matrix[i][j]
    return rank

def generate_random_branching_program(size):
    program = []
    for _ in range(size):
        program.append(random.choice(['0', '1']))
    return program

def construct_tropical_algebraic_stack(program):
    n = len(program)
    stack = [[0] * (n + 1) for _ in range(n + 1)]
    stack[0][0] = 0
    for i in range(1, n + 1):
        if program[i - 1] == '0':
            stack[i][i] = max(stack[i - 1][i], stack[i - 1][i - 1])
        else:
            stack[i][i] = max(stack[i - 1][i], stack[i - 1][i + 1])
    return stack

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            program = generate_random_branching_program(n)
            stack = construct_tropical_algebraic_stack(program)
            rank_value = rank(stack)
            results.append(rank_value)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    
    conjecture_holds = abs(mean_rank - math.log(len(program))) < 3
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank}, expected Θ(log(n))"
    
    return {
        "metric_name": "Rank of Tropical Algebraic Stack",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")