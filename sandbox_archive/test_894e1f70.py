# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([-variables[i-1], variables[j-1]])
                clauses.append([-variables[j-1], variables[i-1]])
        return variables, clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {**assignment, literal: True} if literal > 0 else {**assignment, -literal: False}
            return dpll(clauses, new_assignment)
        
        literal = next((c[0] for c in clauses if c[0] > 0), None)
        if not literal:
            return False
        
        new_clauses_true = [c for c in clauses if literal not in c]
        new_clauses_false = [[-literal]] + [c for c in clauses if -literal not in c]
        
        return dpll(new_clauses_true, {**assignment, literal: True}) or dpll(new_clauses_false, {**assignment, literal: False})
    
    def geometric_invariant(formula):
        variables, clauses = formula
        # Simplified geometric invariant calculation (placeholder)
        return len(variables)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    proofs = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        if not dpll(clauses):
            return {
                "metric_name": "Minimal Rank@Configuration Space",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "DPLL failed to find a model"
            }
        
        rank = geometric_invariant((variables, clauses))
        ranks.append(rank)
        proofs.append(len(clauses))
    
    if len(ranks) < 30:
        return {
            "metric_name": "Minimal Rank@Configuration Space",
            "metric_value": None,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (proofs[i] - mean_proofs) for i in range(len(proofs))) / math.sqrt(sum((ranks[i] - mean_ranks) ** 2 for i in range(len(ranks)))) * math.sqrt(sum((proofs[i] - mean_proofs) ** 2 for i in range(len(proofs))))
    mean_absolute_difference = sum(abs(ranks[i] - predictions[i]) for i in range(len(ranks))) / len(ranks)
    
    return {
        "metric_name": "Minimal Rank@Configuration Space",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample=\"correlation_coefficient<0.8 or mean_absolute_difference>3\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)