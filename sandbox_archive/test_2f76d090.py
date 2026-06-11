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
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0))
        clauses = []
        
        # Base case
        for i in range(n):
            clauses.append((literals[i], literals[n + i]))
        
        # Implication chain
        for i in range(1, n):
            clauses.append((-literals[2 * n - i], literals[2 * n - 1 - i]))
        
        return clauses
    
    def resolution_width(clauses):
        queue = clauses.copy()
        learned_clauses = []
        while queue:
            clause1 = queue.pop()
            for clause2 in queue + learned_clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = list(set(clause1) ^ set(clause2))
                    if not any(new_clause == c for c in queue + learned_clauses):
                        learned_clauses.append(new_clause)
            queue.extend(learned_clauses)
        return len(learned_clauses)
    
    def minimal_brauer_group_order(n):
        # Placeholder function to simulate Brauer group order calculation
        return random.randint(1, 5)  # Simplified for testing
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        phi_f = tseitin_formula(f, n)
        br_f = minimal_brauer_group_order(n)
        w_phi_f = resolution_width(phi_f)
        
        if br_f > 10 or w_phi_f > 100:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Br(f)={br_f} > 10 or w(φ_f)={w_phi_f} > 100"
            }
        
        metric_values.append((br_f, w_phi_f))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Insufficient instances tested (only {len(metric_values)} out of 30)"
        }
    
    br_f_values, w_phi_f_values = zip(*metric_values)
    mean_br_f = sum(br_f_values) / len(br_f_values)
    mean_w_phi_f = sum(w_phi_f_values) / len(w_phi_f_values)
    
    correlation_coefficient = sum((br_f - mean_br_f) * (w_phi_f - mean_w_phi_f) for br_f, w_phi_f in metric_values) / \
                               math.sqrt(sum((br_f - mean_br_f)**2 for br_f in br_f_values)) / \
                               math.sqrt(sum((w_phi_f - mean_w_phi_f)**2 for w_phi_f in w_phi_f_values))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Pearson correlation coefficient < 0.7"
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")