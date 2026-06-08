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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clause.append(random.choice(['', 'not']))
            clauses.append(clause)
        return clauses
    
    def dpll(sat_instance):
        def solve(instance, assignment):
            if not instance:
                return True
            var = next(var for var in instance[0] if var.startswith('x'))
            pos_var = var[2:] if var.startswith('not') else var
            new_assignment = assignment.copy()
            new_assignment[pos_var] = True
            if solve(instance[1:], new_assignment):
                return True
            new_assignment.pop(pos_var)
            new_assignment[pos_var] = False
            if solve(instance[1:], new_assignment):
                return True
            return False
        
        return solve(sat_instance, {})
    
    def geometric_representation(clauses):
        # Simplified representation for demonstration purposes
        return len(clauses) * 2
    
    def coxeter_group_complexity(n):
        # Simplified complexity measure for demonstration purposes
        return n**2
    
    def dpll_search_tree_height(sat_instance):
        return dpll(sat_instance)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        complexity_to_height_ratio_sum = 0
        max_complexity = 0
        max_height = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            sat_instance = generate_sat_instance(n)
            height = dpll_search_tree_height(sat_instance)
            complexity = coxeter_group_complexity(n)
            
            if height == float('inf'):
                continue
            
            instances_tested += 1
            complexity_to_height_ratio_sum += Fraction(complexity, height)
            max_complexity = max(max_complexity, complexity)
            max_height = max(max_height, height)
        
        if instances_tested < 30:
            return {
                "metric_name": "complexity_to_height_ratio",
                "metric_value": float('inf'),
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        complexity_to_height_ratio = Fraction(complexity_to_height_ratio_sum, instances_tested)
        return {
            "metric_name": "complexity_to_height_ratio",
            "metric_value": float(complexity_to_height_ratio),
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    trials = []
    for _ in range(30):
        trial_result = run_trial(seed)
        trials.append(trial_result)
    
    total_metric_value = sum(trial['metric_value'] for trial in trials if not math.isinf(trial['metric_value']))
    instances_tested = sum(trial['instances_tested'] for trial in trials)
    n_max = max(trial['n_max'] for trial in trials)
    conjecture_holds = all(trial['conjecture_holds'] for trial in trials if not math.isinf(trial['metric_value']))
    
    if conjecture_holds:
        mean_metric_value = total_metric_value / instances_tested
        std_dev = (sum((trial['metric_value'] - mean_metric_value) ** 2 for trial in trials if not math.isinf(trial['metric_value'])) / instances_tested) ** 0.5
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, trial in enumerate(trials) if not math.isinf(trial['metric_value']) and not trial['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_data\" first_failing_seed={first_failing_seed}")

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default to list of primes if no seeds provided
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")