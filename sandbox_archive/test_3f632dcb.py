# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = set()
        while len(clauses) < k:
            clause = tuple(random.sample(range(1, n+1), 2))
            if clause not in clauses and (-clause[0], -clause[1]) not in clauses and (-clause[1], -clause[0]) not in clauses:
                clauses.add(clause)
        return clauses

    def frege_proof_length(k_cnf):
        # Simplified model of Frege proof length
        return len(k_cnf) * 5 + random.randint(0, 10)

    def hopf_algebroid_representation(k_cnf):
        # Placeholder for Hopf algebroid representation
        crossed_products = len(k_cnf)
        return crossed_products

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_crossed_products = 0
        total_proof_lengths = 0
        
        while instances_tested < 30:
            k_cnf = generate_k_cnf(n, random.randint(1, n))
            crossed_products = hopf_algebroid_representation(k_cnf)
            proof_length = frege_proof_length(k_cnf)
            
            if crossed_products == 0 or proof_length == 0:
                continue
            
            instances_tested += 1
            total_crossed_products += crossed_products
            total_proof_lengths += proof_length
        
        if instances_tested < 30:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_crossed_products = total_crossed_products / instances_tested
        mean_proof_lengths = total_proof_lengths / instances_tested
        correlation_coefficient = (instances_tested * sum(cp * pl for cp, pl in zip(total_crossed_products, total_proof_lengths)) -
                                   instances_tested * mean_crossed_products * mean_proof_lengths) / \
                                  ((instances_tested - 1) *
                                   (sum(cp**2 for cp in total_crossed_products) - instances_tested * mean_crossed_products**2) *
                                   (sum(pl**2 for pl in total_proof_lengths) - instances_tested * mean_proof_lengths**2))**0.5
        
        results.append(correlation_coefficient)
    
    if all(0.5 <= corr <= 2 for corr in results):
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": sum(results) / len(results),
            "instances_tested": 30 * len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": sum(results) / len(results),
            "instances_tested": 30 * len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "out_of_range"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is not None for result in results):
        mean_value = sum(results) / len(results)
        std_value = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
        support_fraction = sum(1 for r in results if 0.5 <= r <= 2) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(next(r for r in results if not (0.5 <= r <= 2)))]
            print(f"RESULT: FALSIFIED counterexample='out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")