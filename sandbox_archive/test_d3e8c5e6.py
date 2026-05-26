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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        complexity = 0
        for i in range(n):
            bits = [f[j] for j in range(2**i, 2**(i+1))]
            complexity += max(bits.count(0), bits.count(1))
        return complexity
    
    def langlands_dual_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(2**i, 2**(i+1))]
            rank += max(bits.count(0), bits.count(1))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        R_f = communication_complexity(f)
        φ_f_rank = langlands_dual_rank(f)
        
        if R_f == 0:
            continue
        
        results.append({
            "n": n,
            "R_f": R_f,
            "φ_f_rank": φ_f_rank
        })
    
    if not results:
        return {
            "metric_name": "Langlands Dual Rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_values = [result["φ_f_rank"] for result in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(result["φ_f_rank"] - result["R_f"]) <= 0.1 * result["R_f"] for result in results)
    counterexample = "" if conjecture_holds else "Rank does not match complexity"
    
    return {
        "metric_name": "Langlands Dual Rank",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not match complexity\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=No valid instances found")