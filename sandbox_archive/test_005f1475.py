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
    
    def generate_symmetric_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        # Placeholder implementation for communication complexity rank
        # This is a dummy function and should be replaced with actual computation
        return len(f)
    
    def symplectic_grassmannian_order(n):
        # Placeholder implementation for symplectic Grassmannian order
        # This is a dummy function and should be replaced with actual computation
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_symmetric_boolean_function(n)
        mol = symplectic_grassmannian_order(n)
        R_f = communication_complexity_rank(f)
        results.append((mol, R_f))
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mol_values = [mol for mol, _ in results]
    R_f_values = [R_f for _, R_f in results]
    
    sum_mol = sum(mol_values)
    sum_R_f = sum(R_f_values)
    sum_mol_squared = sum(mol**2 for mol in mol_values)
    sum_R_f_squared = sum(R_f**2 for R_f in R_f_values)
    sum_mol_R_f = sum(mol * R_f for mol, R_f in results)
    
    n = len(results)
    mean_mol = sum_mol / n
    mean_R_f = sum_R_f / n
    var_mol = (sum_mol_squared - n * mean_mol**2) / n
    var_R_f = (sum_R_f_squared - n * mean_R_f**2) / n
    cov_mol_R_f = (sum_mol_R_f - n * mean_mol * mean_R_f) / n
    
    correlation_coefficient = cov_mol_R_f / math.sqrt(var_mol * var_R_f)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")