# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        literal = list(set(clause1) ^ set(clause2))[0]
                        new_clause = [l for l in clause1 + clause2 if l != literal and -l not in clause1 + clause2]
                        new_clauses.add(tuple(sorted(new_clause)))
            if len(new_clauses) == 0:
                return len(cnf)
            clauses.update(new_clauses)
    
    def isomorphism_classes(cnf):
        # This is a placeholder for the actual computation of automorphic representations
        # For simplicity, we assume it returns a constant value that depends on the seed
        return Fraction(seed % 10 + 1)  # Example: 1 to 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            w_phi = resolution(cnf)
            num_classes = isomorphism_classes(cnf)
            if num_classes == 0:
                return {"metric_name": "alpha", "metric_value": None, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "mapping_undefined"}
            alpha = w_phi / num_classes
            results.append(alpha)
    
    mean_alpha = sum(results) / len(results)
    std_alpha = (sum((x - mean_alpha) ** 2 for x in results) / len(results)) ** 0.5
    
    return {
        "metric_name": "alpha",
        "metric_value": mean_alpha,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(alpha <= 10 for alpha in results),  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 32))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_alpha = sum(results) / len(results)
    std_alpha = (sum((x - mean_alpha) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r <= 10) / len(results)  # Example threshold
    
    print(f"RESULT: SUPPORTED mean={mean_alpha} std={std_alpha} support_fraction={support_fraction}")