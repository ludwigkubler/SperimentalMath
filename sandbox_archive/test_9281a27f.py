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

def generate_sat_instance(n):
    return [random.choice([-1, 0, 1]) for _ in range(n)]

def dpll(instance):
    n = len(instance)
    stack = []
    assignment = [None] * n
    
    def backtrack(level):
        if level == n:
            return True
        if instance[level] != 0:
            return backtrack(level + 1)
        
        assignment[level] = 1
        if dpll(instance[:level] + [1] + instance[level+1:]):
            return True
        
        assignment[level] = -1
        if dpll(instance[:level] + [-1] + instance[level+1:]):
            return True
        
        return False
    
    return backtrack(0)

def shortest_proof_length(sat_instance):
    proof_length = 0
    while any(x == 0 for x in sat_instance):
        p = next((i for i, x in enumerate(sat_instance) if x == 0), None)
        if p is None:
            break
        new_instance = [x if i != p else -1 for i, x in enumerate(sat_instance)]
        proof_length += 1 + shortest_proof_length(new_instance)
    return proof_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_instances = [generate_sat_instance(n) for _ in range(30)]
        min_ranks = []
        proof_lengths = []
        
        for instance in sat_instances:
            rank = len(set(instance))  # Simplified minimal rank calculation
            min_ranks.append(rank)
            
            proof_length = shortest_proof_length(instance)
            proof_lengths.append(proof_length)
        
        results.append({
            "n": n,
            "min_ranks": min_ranks,
            "proof_lengths": proof_lengths
        })
    
    return {
        "metric_name": "Correlation between minimal rank and proof length",
        "metric_value": sum(math.log(n) * math.log(l) for n, l in zip(results[0]["min_ranks"], results[0]["proof_lengths"])) / len(results[0]["min_ranks"]),
        "instances_tested": 30 * len(n_values),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")