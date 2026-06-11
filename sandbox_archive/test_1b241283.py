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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quantum_state(phi):
        n = len(phi)
        state = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if phi[i ^ j] == 1:
                    state[i][j] = 1
        return state
    
    def min_rank(state):
        n = len(state)
        rank = 0
        for i in range(n):
            row = [state[j][i] for j in range(n)]
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity(phi):
        n = len(phi)
        max_comm = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if phi[i] != phi[j]:
                    comm = bin(i ^ j).count('1')
                    if comm > max_comm:
                        max_comm = comm
        return max_comm
    
    def rank_variance(phi):
        n = len(phi)
        comm = communication_complexity(phi)
        return (comm - 2)**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    rank_vars = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        state = compute_quantum_state(phi)
        min_rank_value = min_rank(state)
        rank_var_value = rank_variance(phi)
        
        min_ranks.append(min_rank_value)
        rank_vars.append(rank_var_value)
    
    if not min_ranks or not rank_vars:
        return {
            "metric_name": "min_rank vs rank_var",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(min_ranks)
    mean_min_rank = sum(min_ranks) / n
    mean_rank_var = sum(rank_vars) / n
    
    def linear_regression(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean)**2 for i in range(n))
        
        if denominator == 0:
            return None, None
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
    
    slope, _ = linear_regression(min_ranks, rank_vars)
    
    if slope is None:
        return {
            "metric_name": "min_rank vs rank_var",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "min_rank vs rank_var",
        "metric_value": slope,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(slope) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all(results):
        return
    
    mean_slope = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not abs(result["metric_value"]) >= 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"slope too low\" first_failing_seed={first_failing_seed}")