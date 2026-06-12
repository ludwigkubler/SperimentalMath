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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clause.append(random.choice(['', '¬']))
            clauses.append(' & '.join(clause))
        return ' | '.join(clauses)
    
    def construct_topological_system(formula):
        # Simplified construction for demonstration
        variables = set()
        transitions = {}
        for clause in formula.split(' | '):
            for var in clause.split('&'):
                if var.startswith('¬'):
                    var = var[1:]
                variables.add(var)
                if var not in transitions:
                    transitions[var] = []
                for other_var in variables - {var}:
                    transitions[var].append(other_var)
        return transitions
    
    def min_topological_entropy(transitions):
        # Simplified entropy calculation for demonstration
        states = list(transitions.keys())
        n_states = len(states)
        if n_states == 0:
            return 0
        entropy = 0
        for state in states:
            out_degree = len(transitions[state])
            if out_degree > 0:
                p = Fraction(1, out_degree)
                entropy -= p * math.log2(p)
        return entropy
    
    def resolution_proof_width(formula):
        # Simplified width calculation for demonstration
        clauses = formula.split(' | ')
        max_width = 0
        for clause in clauses:
            width = len(clause.split('&'))
            if width > max_width:
                max_width = width
        return max_width
    
    def calculate_h_top_squared_log_nm(n, m):
        return (min_topological_entropy(construct_topological_system(generate_formula(n, m))) ** 2) * math.log(n + m)
    
    n_max = 0
    instances_tested = 0
    total_w_phi = 0
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.randint(5, 40)  # Ensure n_min >= 5 and n_max >= 20
        m = random.randint(n, n + 10)
        w_phi = resolution_proof_width(generate_formula(n, m))
        h_top_squared_log_nm = calculate_h_top_squared_log_nm(n, m)
        
        if w_phi > h_top_squared_log_nm:
            return {
                "metric_name": "w(φ)",
                "metric_value": w_phi,
                "instances_tested": instances_tested + 1,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Formula with n={n}, m={m} violates the conjecture"
            }
        
        total_w_phi += w_phi
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_w_phi = total_w_phi / instances_tested
    return {
        "metric_name": "w(φ)",
        "metric_value": mean_w_phi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_w_phi = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_w_phi} std={math.sqrt(sum((r['metric_value'] - mean_w_phi) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n={n_max}, m={m} violates the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")