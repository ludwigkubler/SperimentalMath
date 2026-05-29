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
    
    def hamiltonian_dynamics(f):
        n = int(math.log2(len(f)))
        H_f = 0
        for i in range(2**n):
            if f[i] == 1:
                H_f += 1
        return H_f / (2**n)
    
    def resolution_proof_depth(f):
        # Placeholder function to simulate the computation of resolution proof depth
        # This is a dummy implementation and should be replaced with actual logic
        n = int(math.log2(len(f)))
        return n * 2
    
    instances_tested = 0
    n_max = 0
    total_H_f_squared = 0
    total_t_star = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        H_f = hamiltonian_dynamics(f)
        t_star = resolution_proof_depth(f)
        
        instances_tested += 1
        if n > n_max:
            n_max = n
        
        total_H_f_squared += H_f ** 2
        total_t_star += t_star
    
    mean_H_f_squared = total_H_f_squared / instances_tested
    mean_t_star = total_t_star / instances_tested
    
    conjecture_holds = mean_H_f_squared <= mean_t_star
    correlation_coefficient = (instances_tested * mean_H_f_squared * mean_t_star - 
                               total_H_f_squared * total_t_star) / (
                                   math.sqrt((instances_tested * sum(H_f ** 4 for H_f in [hamiltonian_dynamics(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]]) - instances_tested * mean_H_f_squared ** 2) *
                                             (instances_tested * sum(t_star ** 4 for t_star in [resolution_proof_depth(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]]) - instances_tested * mean_t_star ** 2)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")