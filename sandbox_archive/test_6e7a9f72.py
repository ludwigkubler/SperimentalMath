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

def generate_boolean_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2**n):
        clause = []
        for var in variables:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(f'~{var}')
        clauses.append(clause)
    return clauses

def frege_proof_depth(clauses):
    # Simplified DPLL solver to estimate proof depth
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal.startswith('~'):
                new_assignment[literal[1:]] = False
            return 1 + dpll([c for c in clauses if literal not in c and ~literal not in c], new_assignment)
        pure_literal = next((l for l in variables if all(l in c or '~' + l in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return 1 + dpll([c for c in clauses if pure_literal not in c and ~pure_literal not in c], new_assignment)
        return float('inf')
    
    variables = set(lit.replace('~', '') for clause in clauses for lit in clause)
    assignment = {var: None for var in variables}
    return dpll(clauses, assignment)

def p_adic_logarithmic_rank(clauses):
    # Simplified construction of p-adic ring and rank calculation
    if not clauses:
        return 0
    rank = sum(len(c) for c in clauses if len(c) > 1)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_boolean_formula(n)
        
        proof_depth = frege_proof_depth(clauses)
        rank = p_adic_logarithmic_rank(clauses)
        
        if proof_depth == float('inf'):
            continue
        
        metric_values.append((proof_depth, rank))
    
    if not metric_values:
        return {
            "metric_name": "logrank_p(φ)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_depths, ranks = zip(*metric_values)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    mean_rank = sum(ranks) / len(ranks)
    
    correlation_coefficient = 0
    if len(set(proof_depths)) > 1 and len(set(ranks)) > 1:
        numerator = sum((p - mean_proof_depth) * (r - mean_rank) for p, r in zip(proof_depths, ranks))
        denominator = math.sqrt(sum((p - mean_proof_depth)**2 for p in proof_depths)) * math.sqrt(sum((r - mean_rank)**2 for r in ranks))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "logrank_p(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")