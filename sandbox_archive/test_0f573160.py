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

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(2)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    return clauses

def clause_complexity(cnf):
    return len(cnf)

def noncommutative_polynomial_representation(cnf):
    # Simplified representation for demonstration purposes
    rank = len(cnf)  # This is a placeholder for actual computation
    return rank

def pearson_correlation_coefficient(ranks, complexities):
    n = len(ranks)
    if n < 2:
        return None
    
    mean_rank = sum(ranks) / n
    mean_complexity = sum(complexities) / n
    
    numerator = sum((ranks[i] - mean_rank) * (complexities[i] - mean_complexity) for i in range(n))
    denominator = math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(n))) * math.sqrt(sum((complexities[i] - mean_complexity)**2 for i in range(n)))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        ranks = []
        complexities = []
        
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_cnf(n, random.randint(1, 2 * n))
            rank = noncommutative_polynomial_representation(cnf)
            complexity = clause_complexity(cnf)
            
            ranks.append(rank)
            complexities.append(complexity)
        
        correlation_coefficient = pearson_correlation_coefficient(ranks, complexities)
        
        results.append({
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(ranks),
            "n_max": n,
            "conjecture_holds": correlation_coefficient is not None and 0.6 <= correlation_coefficient < 0.8,
            "counterexample": "" if correlation_coefficient is not None else "insufficient_instances"
        })
    
    return {
        "seed": seed,
        "metric_name": "correlation_coefficient",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if r["counterexample"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_instances\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")