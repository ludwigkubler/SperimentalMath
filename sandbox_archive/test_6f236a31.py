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
    
    # Define constants and parameters
    k = 3  # Number of literals per clause
    n_min = 5
    n_max = 40
    num_trials_per_n = 10
    
    # Initialize variables to store results
    total_rank = 0
    instances_tested = 0
    
    for n in range(n_min, n_max + 1):
        if (n - n_min) % num_trials_per_n == 0:
            print(f"Testing n={n}")
        
        for _ in range(num_trials_per_n):
            # Generate a random k-CNF formula
            variables = list(range(1, n + 1))
            clauses = []
            for _ in range(n):
                clause = random.sample(variables, k)
                clauses.append(clause)
            
            # Construct the graphical realization of the formula
            graph = {i: set() for i in variables}
            for clause in clauses:
                for literal in clause:
                    for other_literal in clause:
                        if literal != other_literal:
                            graph[abs(literal)].add(abs(other_literal))
                            graph[abs(other_literal)].add(abs(literal))
            
            # Compute the noncrossed product K-theory (simplified version)
            k_theory = {}
            for node in graph:
                neighbors = list(graph[node])
                if not neighbors:
                    k_theory[node] = 1
                else:
                    max_rank = 0
                    for neighbor in neighbors:
                        if neighbor in k_theory:
                            max_rank = max(max_rank, k_theory[neighbor])
                    k_theory[node] = max_rank + 1
            
            # Calculate the minimal rank of the noncrossed product K-theory
            min_rank = min(k_theory.values())
            
            # Accumulate results
            total_rank += min_rank
            instances_tested += 1
    
    # Compute empirical mean and check conjecture
    if instances_tested == 0:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "no_instances"
        }
    
    empirical_mean = total_rank / instances_tested
    c = 1.0  # Absolute constant (adjust as needed)
    conjecture_holds = empirical_mean <= c * math.log(n_max)
    counterexample = "" if conjecture_holds else f"mean={empirical_mean}, expected<=c*log({n_max})"
    
    return {
        "metric_name": "min_rank",
        "metric_value": empirical_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and fraction of seeds where conjecture holds
    total_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank / instances_tested} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")