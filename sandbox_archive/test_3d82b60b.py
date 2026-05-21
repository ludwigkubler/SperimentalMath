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
    
    def generate_hyperbolic_surface(g):
        if g < 1:
            return None
        # Simplified model for generating a hyperbolic surface with genus g
        return [random.randint(0, 1) for _ in range(g)]
    
    def satisfiability_problem(surface, n):
        # Simplified model for creating an instance of the satisfiability problem
        variables = list(range(n))
        clauses = []
        for i in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return surface, variables, clauses
    
    def monotone_circuit_size(surface, variables, clauses):
        # Simplified model for estimating the size of a monotone circuit
        return len(clauses) * len(variables)
    
    genus_values = [1, 2, 3, 4]
    results = []
    
    for g in genus_values:
        surface = generate_hyperbolic_surface(g)
        if not surface:
            continue
        
        n = random.randint(5, 40)
        surface, variables, clauses = satisfiability_problem(surface, n)
        circuit_size = monotone_circuit_size(surface, variables, clauses)
        
        D = 2
        bound = D ** g * circuit_size
        
        results.append({
            "g": g,
            "n": n,
            "circuit_size": circuit_size,
            "bound": bound,
            "ratio": abs(bound / circuit_size) if circuit_size != 0 else float('inf')
        })
    
    total_ratio = sum(result["ratio"] for result in results)
    avg_ratio = total_ratio / len(results)
    
    conjecture_holds = all(result["ratio"] <= 1.05 for result in results)
    counterexample = "" if conjecture_holds else "genus={}, n={}, ratio={}".format(
        results[0]["g"], results[0]["n"], results[0]["ratio"]
    )
    
    return {
        "metric_name": "Ratio of Circuit Size to Bound",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {{\"seed\": {}, \"metric_name\": \"Ratio of Circuit Size to Bound\", \"metric_value\": {:.4f}, \"instances_tested\": {}, \"conjecture_holds\": {}, \"counterexample\": \"{}}}".format(
            seed, trial_result["metric_value"], trial_result["instances_tested"], trial_result["conjecture_holds"], trial_result["counterexample"]
        ))
    
    avg_ratio = sum(trial_result["metric_value"] for trial_result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={:.4f} std=0.0000 support_fraction={:.2%}".format(avg_ratio, 0.0000, support_fraction))
    elif any(abs(result["ratio"] - 1) > 0.05 for result in results):
        print("RESULT: FALSIFIED counterexample=\"genus={}, n={}, ratio={}\" first_failing_seed={}".format(
            results[0]["g"], results[0]["n"], results[0]["ratio"], seeds[results.index(next(result for result in results if abs(result["ratio"] - 1) > 0.05))]
        ))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")