# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_matrix_product_state(depth):
    n = 2 ** depth
    state = [[0] * n for _ in range(n)]
    state[0][0] = 1
    return state

def compute_kahler_potential(matrix_product_state):
    n = len(matrix_product_state)
    kahler_potential = 0
    for i in range(n):
        for j in range(n):
            if matrix_product_state[i][j] != 0:
                kahler_potential += math.log(abs(matrix_product_state[i][j]))
    return kahler_potential

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_tests = 30
    total_rank = 0
    total_depth = 0
    
    for _ in range(n_tests):
        depth = random.randint(5, 40)
        matrix_product_state = generate_matrix_product_state(depth)
        kahler_potential = compute_kahler_potential(matrix_product_state)
        rank = len([x for x in kahler_potential if x != 0])
        
        total_rank += rank
        total_depth += depth
    
    mean_rank = total_rank / n_tests
    mean_depth = total_depth / n_tests
    difference = abs(mean_rank - mean_depth)
    
    conjecture_holds = difference <= 1
    counterexample = "" if conjecture_holds else f"mean_diff={difference}"
    
    return {
        "metric_name": "Mean Difference",
        "metric_value": difference,
        "instances_tested": n_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_difference = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_difference} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_difference} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeds_1\" first_failing_seed={first_failing_seed}")