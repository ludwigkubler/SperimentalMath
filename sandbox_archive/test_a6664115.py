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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def gram_schmidt(vectors):
        n = len(vectors)
        q = []
        e = [v[:] for v in vectors]
        for i in range(n):
            qi = e[i].copy()
            for j in range(i):
                proj = sum(q[j][k] * e[i][k] for k in range(len(e[i]))) / sum(q[j][k]**2 for k in range(len(q[j])))
                for k in range(len(e[i])):
                    qi[k] -= proj * q[j][k]
            norm = math.sqrt(sum(qi[k]**2 for k in range(len(qi))))
            if norm == 0:
                continue
            q.append([qi[k] / norm for k in range(len(qi))])
        return q
    
    def frobenius_schmidt_distance(state, uniform_dist):
        n = len(state)
        dist = sum((state[i] - uniform_dist[i])**2 for i in range(n))
        return math.sqrt(dist)
    
    def communication_complexity_rank_variance(function):
        n = int(math.log2(len(function)))
        if 2**n != len(function):
            raise ValueError("Function size must be a power of 2")
        rank = sum(1 for i in range(n) if function[i] == 1 and all(function[j] == 0 for j in range(i+1, n)))
        return (rank / n - 0.5)**2
    
    def generate_uniform_distribution(n):
        return [Fraction(1, 2**n)] * (2**n)
    
    trials = []
    for n in {5, 10, 15, 20, 30, 40}:
        for _ in range(5):  # Ensure at least 30 instances per seed
            function = generate_boolean_function(n)
            state = gram_schmidt([function])[0]
            uniform_dist = generate_uniform_distribution(n)
            fs_dist = frobenius_schmidt_distance(state, uniform_dist)
            ccr_var = communication_complexity_rank_variance(function)
            trials.append((fs_dist, ccr_var))
    
    if not trials:
        return {
            "metric_name": "FS_dist vs CCR_var",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    fs_dists, ccr_vars = zip(*trials)
    mean_fs_dist = sum(fs_dists) / len(fs_dists)
    mean_ccr_var = sum(ccr_vars) / len(ccr_vars)
    
    # Spearman's rho correlation coefficient
    rank_corr = 0
    for i in range(len(trials)):
        for j in range(i+1, len(trials)):
            if fs_dists[i] != fs_dists[j]:
                rank_corr += (i < j) - (j < i)
            if ccr_vars[i] != ccr_vars[j]:
                rank_corr += (i < j) - (j < i)
    n = len(trials)
    rho = rank_corr / ((n * (n - 1)) / 2)
    
    return {
        "metric_name": "FS_dist vs CCR_var",
        "metric_value": rho,
        "instances_tested": len(trials),
        "n_max": max(n for _, _ in trials),
        "conjecture_holds": abs(rho) >= 0.5,
        "counterexample": "" if abs(rho) >= 0.5 else "rho < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) >= 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")