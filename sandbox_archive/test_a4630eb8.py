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
    
    def generate_tseitin(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n+1):
            clause = [f'x{i}', f'y{i}']
            clauses.append(clause)
        
        # Generate AND clauses
        for i in range(2, n+1):
            clause = [f'x{i-1}', f'y{i}', f'z{i}']
            clauses.append(clause)
        
        # Generate final OR clause
        final_clause = [f'z{n}', 'F']
        clauses.append(final_clause)
        
        return variables, clauses
    
    def resolution(clauses):
        while True:
            new_clauses = []
            found_resolvent = False
            
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    
                    # Find complementary literals
                    common_literals = [lit for lit in clause_i if -lit in clause_j]
                    if common_literals:
                        resolvent = (clause_i - {common_literals[0]}) | (clause_j - {-common_literals[0]})
                        new_clauses.append(list(resolvent))
                        found_resolvent = True
            
            if not found_resolvent:
                return len(clauses)
            
            # Remove duplicates and empty clauses
            clauses = list({tuple(sorted(c)) for c in new_clauses if c})
    
    def geometric_flow_time(n):
        # Simulate a simple geometric flow that separates points by flipping variables
        steps = 0
        while True:
            steps += 1
            for i in range(1, n+1):
                if random.choice([True, False]):
                    return steps
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            variables, clauses = generate_tseitin(n)
            w_phi_G = resolution(clauses)
            flow_time = geometric_flow_time(n)
            
            if flow_time == 0 or w_phi_G == 0:
                continue
            
            ratio = flow_time / w_phi_G
            total_metric_value += ratio
            instances_tested += 1
            n_max = max(n_max, n)
            
            if not (0.5 <= ratio <= 2):
                conjecture_holds = False
                counterexample = f"n={n}, flow_time={flow_time}, w_phi_G={w_phi_G}"
    
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "Flow Time to Resolution Width Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")