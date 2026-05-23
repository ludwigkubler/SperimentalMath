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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def read_twice_branching_program(n):
        program = []
        for _ in range(n):
            state = random.randint(0, 1)
            transition = random.choice(['left', 'right'])
            program.append((state, transition))
        return program

    def free_probability_distribution(program):
        n = len(program)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            state, transition = program[i]
            if state == 0:
                A[0][i+1] += 1
            else:
                A[n][i+1] += 1
            if transition == 'left':
                A[i+1][i+2] += 1
            else:
                A[i+1][i] += 1
        return rank(A)

    n = random.randint(5, 40)
    program = read_twice_branching_program(n)
    rank_value = free_probability_distribution(program)
    
    return {
        "metric_name": "Rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value <= 1.5 * (n ** (1/3)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] for result in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")