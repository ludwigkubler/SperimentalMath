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
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(0, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def construct_quandle(clauses):
        quandle = {}
        for clause in clauses:
            for literal in clause:
                if literal not in quandle:
                    quandle[literal] = set()
                for other_literal in clause:
                    if other_literal != literal and -other_literal not in quandle[literal]:
                        quandle[literal].add(other_literal)
        return quandle
    
    def calculate_quandle_order(quandle):
        order = 0
        for key, value in quandle.items():
            order += len(value)
        return order
    
    def calculate_clause_complexity(clauses):
        return len(clauses)
    
    instances_tested = 0
    correlation_sum = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested += 2**n - 1
        n_max = max(n_max, n)
        
        for _ in range(2**n - 1):
            clauses = generate_sat_instance(n)
            quandle = construct_quandle(clauses)
            quandle_order = calculate_quandle_order(quandle)
            clause_complexity = calculate_clause_complexity(clauses)
            
            if quandle_order > n**(3/2):
                conjecture_holds = False
                counterexample = f"n={n}, order={quandle_order} exceeds O(n^(3/2))"
                break
            
            correlation_sum += quandle_order * clause_complexity
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_quandle_order = correlation_sum / (2**n - 1)
    std_dev = math.sqrt(sum((quandle_order * clause_complexity - mean_quandle_order) ** 2 for quandle_order, clause_complexity in zip(quandle_orders, clause_complexities)) / (2**n - 1))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_sum,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")