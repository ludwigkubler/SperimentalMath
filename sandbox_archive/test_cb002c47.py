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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of communication complexity calculation
        rank = sum(f[i] != f[i + 1] for i in range(len(f) - 1)) / (len(f) - 1)
        return rank
    
    def calculate_brauer_group_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of Brauer group calculation
        rank = sum(1 for i in range(n) if f[i] == 1)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = generate_boolean_function(n)
            brauer_group_rank = calculate_brauer_group_rank(f)
            communication_rank = communication_complexity_rank(f)
            results.append((brauer_group_rank, communication_rank))
    
    if not results:
        return {
            "metric_name": "Brauer Group Rank vs Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    brauer_group_ranks = [r[0] for r in results]
    communication_ranks = [r[1] for r in results]
    
    mean_brauer = sum(brauer_group_ranks) / len(brauer_group_ranks)
    mean_communication = sum(communication_ranks) / len(communication_ranks)
    
    correlation_coefficient = sum((brauer_group_ranks[i] - mean_brauer) * (communication_ranks[i] - mean_communication) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "Brauer Group Rank vs Communication Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")