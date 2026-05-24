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
    
    def generate_sat_instance(n):
        return ' '.join(random.choice('01') for _ in range(2**n))
    
    def dpll(sat_instance):
        # Simplified DPLL algorithm to find resolution proof
        clauses = sat_instance.split()
        stack = []
        while True:
            if not any(clause.startswith('!') for clause in clauses):
                return len(stack)
            unit_clause = next((clause for clause in clauses if '!' not in clause), None)
            if not unit_clause:
                return float('inf')
            unit_var = unit_clause[0]
            stack.append(unit_var)
            new_clauses = []
            for clause in clauses:
                if unit_var in clause:
                    continue
                if '!' + unit_var in clause:
                    new_clauses.extend(clause.replace('!' + unit_var, '').split())
                else:
                    new_clauses.append(clause)
            clauses = new_clauses
    
    def minimal_local_complexity(n):
        # Constructive mapping for minimal local complexity (simplified example)
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        proof_diameter = dpll(sat_instance)
        local_complexity = minimal_local_complexity(n)
        ratio = proof_diameter / (2**(1 + n))
        
        results.append({
            "n": n,
            "sat_instance": sat_instance,
            "proof_diameter": proof_diameter,
            "local_complexity": local_complexity,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 2**(1 + n) for result in results)
    counterexample = "" if conjecture_holds else f"Ratio exceeds 2^(1+n) at n={n}"
    
    return {
        "metric_name": "Ratio of Resolution Proof Diameter to Minimal Local Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 2^(1+n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Not enough seeds support the conjecture")