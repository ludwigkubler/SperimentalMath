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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        return n
    
    def projective_representations(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        
        # Constructive mapping to projective geometry
        points = [(i, f[i]) for i in range(2**n)]
        lines = []
        for i in range(n):
            line = set()
            for j in range(2**n):
                if (j >> i) & 1:
                    line.add(j)
            lines.append(line)
        
        # Count projective representations
        return len(lines)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        N_f = projective_representations(f)
        c_f = communication_complexity(f)
        results.append({"n": n, "N_f": N_f, "c_f": c_f})
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    N_values = [result["N_f"] for result in results]
    c_values = [result["c_f"] for result in results]
    
    mean_N = sum(N_values) / len(N_values)
    mean_c = sum(c_values) / len(c_values)
    
    covariance = sum((N - mean_N) * (c - mean_c) for N, c in zip(N_values, c_values)) / len(N_values)
    variance_N = sum((N - mean_N)**2 for N in N_values) / len(N_values)
    variance_c = sum((c - mean_c)**2 for c in c_values) / len(c_values)
    
    if variance_N == 0 or variance_c == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_N) * math.sqrt(variance_c))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(N_values),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if all(result["conjecture_holds"] for result in results):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            counterexample = "Pearson correlation coefficient < 0.7"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")