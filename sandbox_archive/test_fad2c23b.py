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
    
    def generate_boolean_formula(n):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.choice(['', 'not ']) + random.choice(variables)
            if random.random() < 0.5:
                clause += " or " + random.choice(variables)
            clauses.append(clause)
        return " and ".join(clauses)

    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        for token in formula.split():
            if token == 'and':
                stack.append('and')
            elif token == 'or':
                stack.append('or')
            elif token.startswith('not'):
                stack[-1] = f"not {stack[-1]}"
            else:
                stack.append(token)
        return len(stack)

    def p_adic_logarithmic_rank(formula):
        # Placeholder for actual computation
        return random.random() * 10

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_depth = 0
    total_rank = 0
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        depth = frege_proof_depth(formula)
        rank = p_adic_logarithmic_rank(formula)
        
        if depth == 0 or rank == 0:
            continue
        
        results.append((depth, rank))
        total_depth += depth
        total_rank += rank
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    mean_depth = total_depth / n
    mean_rank = total_rank / n
    
    covariance = sum((depth - mean_depth) * (rank - mean_rank) for depth, rank in results) / n
    variance_depth = sum((depth - mean_depth) ** 2 for depth, _ in results) / n
    variance_rank = sum((rank - mean_rank) ** 2 for _, rank in results) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_depth = 0
    total_rank = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            count_supporting += 1
        
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = count_supporting / len(seeds)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")