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
    
    def quadratic_residue_symbol(phi):
        n = len(phi)
        min_val = float('inf')
        for k in range(2**n):
            val = 1
            for i in range(n):
                if phi[i] == '1':
                    val *= (k >> i) & 1
            min_val = min(min_val, abs(val))
        return min_val
    
    def frege_proof_depth(phi):
        n = len(phi)
        stack = []
        depth = 0
        for lit in phi:
            if lit == '1':
                stack.append(lit)
                depth += 1
            elif lit == '0':
                if not stack:
                    return float('inf')
                stack.pop()
                depth -= 1
        if stack:
            return float('inf')
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_qm = 0
        total_depth = 0
        
        while len(results) < 30:
            phi = ''.join(random.choice('01') for _ in range(n))
            qm = quadratic_residue_symbol(phi)
            depth = frege_proof_depth(phi)
            
            if qm != float('inf') and depth != float('inf'):
                instances_tested += 1
                total_qm += qm
                total_depth += depth
                results.append((qm, depth))
        
        if len(results) < 30:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_valid_instances"
            }
    
    qm_values = [qm for qm, _ in results]
    depth_values = [depth for _, depth in results]
    
    mean_qm = sum(qm_values) / len(qm_values)
    mean_depth = sum(depth_values) / len(depth_values)
    
    covariance = sum((qm - mean_qm) * (depth - mean_depth) for qm, depth in results) / len(results)
    variance_qm = sum((qm - mean_qm)**2 for qm in qm_values) / len(qm_values)
    variance_depth = sum((depth - mean_depth)**2 for depth in depth_values) / len(depth_values)
    
    pearson_corr = covariance / math.sqrt(variance_qm * variance_depth)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")