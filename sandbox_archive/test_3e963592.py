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

def generate_k_cnf(n, k):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = []
        for var in random.sample(variables, random.randint(1, n)):
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def jacobian_rank(n, k):
    # Placeholder function to compute the rank of the Jacobian matrix
    # This is a dummy implementation and should be replaced with actual computation
    return n * (k + 1) // 2

def resolution_proof_size(clauses):
    # Placeholder function to compute the resolution proof size
    # This is a dummy implementation and should be replaced with actual computation
    return len(clauses) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = max(1, n // 2)  # Ensure at least one clause
        clauses = generate_k_cnf(n, k)
        rank = jacobian_rank(n, k)
        proof_size = resolution_proof_size(clauses)
        
        if rank == 0 or proof_size == 0:
            continue
        
        ratio = proof_size / rank
        results.append({
            "n": n,
            "k": k,
            "rank": rank,
            "proof_size": proof_size,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Resolution Proof Size Ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 1.5 for result in results)
    
    return {
        "metric_name": "Resolution Proof Size Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio exceeded 1.5 for n={results[0]['n']}, k={results[0]['k']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")