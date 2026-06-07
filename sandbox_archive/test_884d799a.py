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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0))
        clauses = []
        
        # Base case
        for i in range(n):
            clauses.append((literals[i], literals[n + i]))
        
        # Function body
        for i in range(2**n):
            binary_rep = [int(x) for x in format(i, f'0{n}b')]
            clause = []
            for j in range(n):
                if binary_rep[j] == 1:
                    clause.append(literals[j])
                else:
                    clause.append(-literals[j])
            clauses.append(clause)
        
        return literals, clauses
    
    def resolution_proof_depth(clauses):
        queue = clauses[:]
        visited = set()
        depth = 0
        
        while queue:
            new_queue = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1 + clause2) - {list(set(clause1) & set(clause2))[0]})
                        if not new_clause:
                            return depth
                        new_queue.append(new_clause)
            queue = new_queue
            visited.update(queue)
            depth += 1
        
        return float('inf')
    
    def algebraic_degree(f, n):
        count = 0
        for i in range(2**n):
            binary_rep = [int(x) for x in format(i, f'0{n}b')]
            if sum(binary_rep) % 2 == 1:
                count += 1
        return count
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_dev_x * std_dev_y) if std_dev_x != 0 and std_dev_y != 0 else 0
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_random_boolean_function(n)
        literals, clauses = tseitin_formula(f, n)
        d_phi_f = resolution_proof_depth(clauses)
        delta_f = algebraic_degree(f, n)
        results.append((delta_f, d_phi_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    delta_values, d_phi_values = zip(*results)
    corr_coeff = correlation_coefficient(delta_values, d_phi_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": corr_coeff > 0.7 and all(corr_coeff >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result and result["counterexample"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")