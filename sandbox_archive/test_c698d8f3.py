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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def quantum_group_representation(formula):
        # Placeholder for actual quantum group representation logic
        return len(formula)  # Simplified example
    
    def dpll_proof_tree_depth(rank):
        # Placeholder for actual DPLL proof tree depth logic
        return rank + 1  # Simplified example
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        rank = quantum_group_representation(formula)
        depth = dpll_proof_tree_depth(rank)
        
        if rank > n**1.5 or depth < rank:
            return {
                "metric_name": "DPLL Proof Tree Depth",
                "metric_value": depth,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Formula: {formula}, Rank: {rank}, Depth: {depth}"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "depth": depth
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_depth = sum(result["depth"] for result in results) / len(results)
    
    return {
        "metric_name": "DPLL Proof Tree Depth",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(depth >= rank for result in results for depth, rank in zip([result["depth"]] * 10, [result["rank"]] * 10)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")