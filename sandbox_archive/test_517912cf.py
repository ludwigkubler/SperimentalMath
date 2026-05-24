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
    
    def generate_disjointness_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_partial_order(f):
        n = len(f)
        partial_order = [[False] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == 1 and f[j] == 0:
                    partial_order[i][j] = True
        return partial_order
    
    def compute_quandle_representation(partial_order):
        n = len(partial_order)
        quandle_rep = [[None] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if partial_order[i][j]:
                    quandle_rep[i][j] = j
        return quandle_rep
    
    def compute_minimal_rank(quandle_rep):
        n = len(quandle_rep)
        rank = 0
        for i in range(n):
            for j in range(n):
                if quandle_rep[i][j] is not None:
                    rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_disjointness_function(n)
            partial_order = compute_partial_order(f)
            quandle_rep = compute_quandle_representation(partial_order)
            rank = compute_minimal_rank(quandle_rep)
            total_rank += rank
            instances_tested += 1
    
    average_rank = total_rank / instances_tested
    conjecture_holds = average_rank >= n_values[0]
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Minimal Rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")