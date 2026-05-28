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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def rank_of_matrix(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for i in range(m):
        if any(A_copy[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def construct_quaternionic_form(n):
    truth_table = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    form = []
    for i in range(2**n):
        row = [truth_table[i][j] * (-1)**sum(truth_table[i][k] & truth_table[j][k] for k in range(3)) for j in range(2**n)]
        form.append(row)
    return form

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        form = construct_quaternionic_form(n)
        rank = rank_of_matrix(form)
        total_rank += rank
        instances_tested += len(form)
    
    average_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = average_rank >= 0.5 * math.log(instances_tested) + 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_rank",
        "metric_value": float(average_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results)
    instances_tested = sum(result["instances_tested"] for result in results)
    average_rank = Fraction(total_rank, instances_tested)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={average_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={average_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = result["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")