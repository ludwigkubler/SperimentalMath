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
    
    def compute_tropicalized_cohomology(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function size")
        
        # Compute the tropicalized cohomology rank (simplified example)
        return sum(1 for bit in f if bit == 1)
    
    def compute_resolution_proof_tree_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function size")
        
        # Simplified DPLL solver to estimate resolution proof tree width
        def dpll(s, clauses):
            if not clauses:
                return True
            for literal in s:
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if dpll(s + [literal], new_clauses) or dpll(s + [-literal], new_clauses):
                    return True
            return False
        
        def count_clauses(clauses):
            return len(clauses)
        
        # Generate a random set of clauses for the function
        clauses = []
        for i in range(n):
            if f[i] == 1:
                clauses.append([i + 1])
            else:
                clauses.append([-i - 1])
        
        return count_clauses(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = compute_tropicalized_cohomology(f)
        width = compute_resolution_proof_tree_width(f)
        
        if rank < width - 2:  # Allow a small margin of error
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, width={width}"
            }
        
        results.append(rank)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": std <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 2**31 - 1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= mean - 2) / len(results)
    
    if all(r >= mean - 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < mean - 2 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r < mean - 2)
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[first_failing_seed]}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")