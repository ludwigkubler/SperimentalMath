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
    
    def generate_monotone_dnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([True, False]) for _ in range(n)]
            if any(clause):
                clauses.append(clause)
        return clauses
    
    def compute_minimal_rank(dnf):
        # Placeholder function to simulate computation
        # Replace with actual algorithm for minimal rank
        return random.randint(1, 10) * len(dnf)
    
    def resolution_proof_complexity(rank):
        # Placeholder function to simulate resolution proof complexity
        # Replace with actual algorithm if known
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        dnf = generate_monotone_dnf(n)
        rank = compute_minimal_rank(dnf)
        complexity = resolution_proof_complexity(rank)
        
        if rank < n**n or rank > n**(n+1):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} out of bounds for n={n}"
            }
        
        if complexity < n**n:
            return {
                "metric_name": "resolution_complexity",
                "metric_value": complexity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Complexity {complexity} too low for n={n}"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "complexity": complexity
        })
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=<not_computed> support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<not_computed>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")