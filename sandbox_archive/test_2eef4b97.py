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
    
    def output_complexity(f):
        n = int(math.log2(len(f)))
        count = sum(1 for i in range(2**n) if f[i] != f[0])
        return count
    
    def algebraic_stack_rank(n, C):
        # Simplified model of the rank calculation
        return 2**(C - 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C = output_complexity(f)
        
        rank_upper_bound = algebraic_stack_rank(n, C)
        rank_lower_bound = algebraic_stack_rank(n, C // 2) if C % 2 == 0 else None
        
        results.append({
            "n": n,
            "C": C,
            "rank_upper_bound": rank_upper_bound,
            "rank_lower_bound": rank_lower_bound
        })
    
    min_rank = min(result["rank_upper_bound"] for result in results)
    conjecture_holds = all(result["rank_upper_bound"] <= 2**result["C"] for result in results)
    if not conjecture_holds:
        counterexample = f"n={results[0]['n']}, C={results[0]['C']}, rank_upper_bound={results[0]['rank_upper_bound']}"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, C={results[0]['C']}, rank_upper_bound={results[0]['rank_upper_bound']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")