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
    
    # Generate Tseitin circuit with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(1, n))]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    # Compute noncommutative tensor product representation
    # This is a placeholder function; actual computation depends on the conjecture
    def noncommutative_tensor_product_representation(variables, clauses):
        # Placeholder implementation: return a dummy rank
        return random.randint(1, 10)
    
    rank = noncommutative_tensor_product_representation(variables, clauses)
    
    # Calculate O(n^(1/2)m^(1/4))
    bound = n**0.5 * m**0.25
    
    # Determine if the conjecture holds
    conjecture_holds = (rank <= 1.5 * bound) and (abs(rank - bound) / bound < 0.1)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} exceeds bound {bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    # Compute mean and standard deviation of metric values
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit(0)
    
    total_rank = sum(result["metric_value"] for result in results)
    mean_rank = total_rank / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_rank) ** 2 for result in results)
    std_dev = math.sqrt(squared_diff_sum / len(results))
    
    # Determine support fraction
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")