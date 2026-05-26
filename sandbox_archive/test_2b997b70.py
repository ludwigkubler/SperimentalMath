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
    
    def generate_random_3sat(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        assignment = {i: None for i in range(1, n + 1)}
        
        def backtrack(i):
            if i > n:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(any(x * assignment[abs(x)] >= 0 for x in clause) for clause in clauses):
                    if backtrack(i + 1):
                        return True
            assignment[i] = None
            return False
        
        return backtrack(1)
    
    def compute_automorphism_group(clauses):
        # Placeholder for actual automorphism group computation
        # This is a dummy implementation that always returns an identity automorphism
        return []
    
    n = random.randint(5, 40)
    clauses = generate_random_3sat(n)
    if not is_satisfiable(clauses):
        return {
            "metric_name": "minimal_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    automorphism_group = compute_automorphism_group(clauses)
    minimal_rank = len(automorphism_group)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not implemented\" first_failing_seed={first_failing_seed}")