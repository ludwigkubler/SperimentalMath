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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def vector_space_basis(f):
        n = len(f)
        basis = []
        for i in range(2**n):
            if f[i] == 1:
                vec = [int(x) for x in format(i, f'0{n}b')]
                if all(vec[j] != basis[j][1] for j in range(n)):
                    basis.append((vec, f[i]))
        return basis
    
    def symplectic_hull_volume(basis):
        n = len(basis[0][0])
        volume = 1
        for i in range(n):
            for j in range(i+1, n):
                dot_product = sum(basis[k][0][i] * basis[k][0][j] for k in range(len(basis)))
                if dot_product != 0:
                    return 0
                volume *= math.sqrt(2)
        return volume
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = sum(1 for i in range(n) if f[i] == 1)
        return (rank - n/2)**2 / n
    
    trials = [(5, 10, 15, 20, 30, 40)]
    results = []
    
    for n in random.choice(trials):
        instances_tested = 0
        total_shv = 0
        total_crv = 0
        
        for _ in range(50):  # Aim for at least 30 instances per seed
            f = generate_random_boolean_function(n)
            basis = vector_space_basis(f)
            shv = symplectic_hull_volume(basis)
            crv = communication_complexity_rank_variance(f)
            
            if shv == 0 or crv == 0:
                continue
            
            total_shv += shv
            total_crv += crv
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "Pearson Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        shv_avg = total_shv / instances_tested
        crv_avg = total_crv / instances_tested
        
        results.append((shv_avg, crv_avg))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    shv_values, crv_values = zip(*results)
    mean_shv = sum(shv_values) / len(shv_values)
    mean_crv = sum(crv_values) / len(crv_values)
    correlation_coefficient = (sum((shv_values[i] - mean_shv) * (crv_values[i] - mean_crv) for i in range(len(shv_values))) /
                                math.sqrt(sum((shv_values[i] - mean_shv)**2 for i in range(len(shv_values))) *
                                          sum((crv_values[i] - mean_crv)**2 for i in range(len(crv_values)))))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in trials),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")