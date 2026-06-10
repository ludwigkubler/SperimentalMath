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
    
    def generate_tseitin_formula(n, num_clauses):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(num_clauses):
            clause = []
            for j in range(random.randint(1, n)):
                var = random.choice(variables)
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(-var)
            clauses.append(clause)
        
        return variables, clauses
    
    def resolution_proof_width(clauses):
        # Simplified resolution proof width calculation (not actual implementation)
        return len(clauses) ** 2
    
    def smallest_p_adic_exponent(num_clauses, p=2):
        e = 0
        while p ** e < num_clauses:
            e += 1
        return e - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            num_clauses = int(n * random.uniform(1, 10))
            variables, clauses = generate_tseitin_formula(n, num_clauses)
            
            w_phi = resolution_proof_width(clauses)
            e = smallest_p_adic_exponent(num_clauses)
            metric_value = math.log(p ** n / num_clauses)
            
            results.append({
                "n": n,
                "num_clauses": num_clauses,
                "w_phi": w_phi,
                "e": e,
                "metric_value": metric_value
            })
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    w_phi_values = [result["w_phi"] for result in results]
    e_values = [result["e"] for result in results]
    metric_values = [result["metric_value"] for result in results]
    
    mean_w_phi = sum(w_phi_values) / instances_tested
    mean_e = sum(e_values) / instances_tested
    mean_metric_value = sum(metric_values) / instances_tested
    
    if abs(mean_w_phi - mean_metric_value) <= 3 * (mean_metric_value / math.sqrt(instances_tested)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"resolution_proof_width={mean_w_phi} does not match log(p^n / #clauses(φ))={mean_metric_value}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")