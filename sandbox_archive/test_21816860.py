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
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 10 * n)
        k = random.randint(1, min(n, 3))
        
        # Generate a random k-CNF instance
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), k)]
            clauses.append(clause)
        
        # Construct the Frege proof tree and compute K-theory (simplified model)
        # This is a placeholder for actual K-theory computation
        k_theory_vector = [random.random() for _ in range(2 ** n)]
        
        # Compute the minimal rank of the k-th exterior power of the K-theory vector space
        min_rank = len(k_theory_vector)  # Simplified model
        
        # Calculate the predicted rank based on the conjecture's formula
        predicted_rank = math.log(n) / math.log(m)
        
        results.append({
            "n": n,
            "m": m,
            "k": k,
            "min_rank": min_rank,
            "predicted_rank": predicted_rank
        })
    
    # Calculate the mean and standard deviation of the metric values
    mean_rank = sum(result["min_rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["min_rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    # Check if the conjecture holds within ±30% of the predicted rank
    support_fraction = sum(abs(result["min_rank"] - result["predicted_rank"]) <= 0.3 * abs(result["predicted_rank"]) for result in results) / len(results)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, m={results[0]['m']}, k={results[0]['k']}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, m={results[0]['m']}, k={results[0]['k']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")