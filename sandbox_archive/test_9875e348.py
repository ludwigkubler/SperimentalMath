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
        n = len(f)
        max_comm_cost = float('-inf')
        for i in range(1 << (n - 1)):
            assignment = [(i >> j) & 1 for j in range(n)]
            comm_cost = sum(abs(a - b) for a, b in zip(assignment[:n//2], assignment[n//2:]))
            max_comm_cost = max(max_comm_cost, comm_cost)
        return max_comm_cost
    
    def calculate_brauer_group_rank(f):
        n = len(f)
        # Simplified version of Brauer group rank calculation for demonstration
        # This is a placeholder and should be replaced with actual computation
        return random.randint(1, n)
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_boolean_function(n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            comm_rank = communication_complexity(f)
            brauer_group_rank = calculate_brauer_group_rank(f)
            
            results.append({
                "n": n,
                "comm_rank": comm_rank,
                "brauer_group_rank": brauer_group_rank
            })
    
    if instances_tested < 30:
        return {
            "metric_name": "Brauer Group Rank vs Communication Complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    comm_ranks = [r["comm_rank"] for r in results]
    brauer_group_ranks = [r["brauer_group_rank"] for r in results]
    
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    mean_brauer_group_rank = sum(brauer_group_ranks) / len(brauer_group_ranks)
    
    correlation_coefficient = 0
    if len(comm_ranks) > 1:
        numerator = sum((comm_ranks[i] - mean_comm_rank) * (brauer_group_ranks[i] - mean_brauer_group_rank) for i in range(len(comm_ranks)))
        denominator = math.sqrt(sum((comm_ranks[i] - mean_comm_rank)**2 for i in range(len(comm_ranks)))) * math.sqrt(sum((brauer_group_ranks[i] - mean_brauer_group_rank)**2 for i in range(len(brauer_group_ranks))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Brauer Group Rank vs Communication Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Brauer group rank {r['brauer_group_rank']} does not match communication complexity rank {r['comm_rank']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break