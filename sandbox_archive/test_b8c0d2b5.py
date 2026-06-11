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

def calculate_padic_valuation_degree(clause, p):
    degrees = [abs(int(literal)) for literal in clause if literal != '1' and literal != '-1']
    return min(degrees) if degrees else float('inf')

def generate_random_cnf(num_clauses, seed):
    random.seed(seed)
    literals = ['1', '-1'] + [str(i) for i in range(2, 10)]
    formula = []
    for _ in range(num_clauses):
        clause = random.sample(literals, 3)
        random.shuffle(clause)
        formula.append(' '.join(clause))
    return formula

def run_trial(seed: int) -> dict:
    num_clauses = 40
    formula = generate_random_cnf(num_clauses, seed)
    clause_depths = [len(clause.split()) for clause in formula]
    min_valuation_degrees = [calculate_padic_valuation_degree(clause, 2) for clause in formula]
    
    if not min_valuation_degrees or not clause_depths:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_val = min(min_valuation_degrees)
    max_val = max(min_valuation_degrees)
    mean_val = sum(min_valuation_degrees) / len(min_valuation_degrees)
    std_dev = math.sqrt(sum((x - mean_val) ** 2 for x in min_valuation_degrees) / len(min_valuation_degrees))
    
    correlation_numerator = sum((min_valuation_degrees[i] - mean_val) * (clause_depths[i] - mean(clause_depths)) for i in range(len(min_valuation_degrees)))
    correlation_denominator = math.sqrt(sum((x - mean_val) ** 2 for x in min_valuation_degrees)) * math.sqrt(sum((y - mean(clause_depths)) ** 2 for y in clause_depths))
    
    if correlation_denominator == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = correlation_numerator / correlation_denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": num_clauses,
        "n_max": num_clauses,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")