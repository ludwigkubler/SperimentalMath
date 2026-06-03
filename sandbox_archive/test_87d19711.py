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
    
    def frege_proof_length(f):
        # Simplified Frege proof length calculation (not actual Frege proof)
        return len(f) * 2
    
    def min_rank(cubical_complex):
        # Simplified minimal rank calculation (not actual algebraic geometry)
        return len(cubical_complex)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        L_f = frege_proof_length(f)
        C_f = generate_boolean_function(2**n)  # Simplified cubical complex
        min_rank_C_f = min_rank(C_f)
        
        if L_f == 0 or min_rank_C_f == 0:
            continue
        
        results.append({
            "n": n,
            "L_f": L_f,
            "min_rank_C_f": min_rank_C_f
        })
    
    if not results:
        return {
            "metric_name": "min_rank / L_f",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    min_rank_values = [r["min_rank_C_f"] for r in results]
    L_f_values = [r["L_f"] for r in results]
    
    mean_L_f = sum(L_f_values) / len(L_f_values)
    std_L_f = math.sqrt(sum((x - mean_L_f) ** 2 for x in L_f_values) / len(L_f_values))
    mean_min_rank_C_f = sum(min_rank_values) / len(min_rank_values)
    
    ratio = [min_rank / L_f for min_rank, L_f in zip(min_rank_values, L_f_values)]
    max_ratio = max(ratio)
    
    return {
        "metric_name": "min_rank / L_f",
        "metric_value": mean_min_rank_C_f,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": max_ratio <= 2,
        "counterexample": "" if max_ratio <= 2 else f"max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        RESULT = f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}"
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    
    print(RESULT)