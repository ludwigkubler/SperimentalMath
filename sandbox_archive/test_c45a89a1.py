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
    
    def generate_random_language(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = set()
            for _ in range(random.randint(1, n)):
                var = chr(ord('a') + random.randint(0, n-1))
                if random.choice([True, False]):
                    clause.add(var)
                else:
                    clause.add(f'~{var}')
            clauses.append(clause)
        return clauses

    def compute_communication_complexity_rank(clauses):
        variables = set()
        for clause in clauses:
            variables.update(clause)
        
        if not variables:
            return 0
        
        # Simulate a commutative group and its representation
        G = []
        for var in variables:
            G.append([1 if v == var else 0 for v in variables])
        
        rank = len(G)
        for i in range(len(G)):
            for j in range(i+1, len(G)):
                if any(var in clauses[i] and var in clauses[j] for var in variables):
                    rank += 1
        
        return rank

    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 instances
            clauses = generate_random_language(n)
            rank = compute_communication_complexity_rank(clauses)
            results.append(rank)
    
    mean_variance = sum(results) / len(results)
    conjecture_holds = all(x >= math.log(n) for x, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "variance_less_than_log_n"
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_variance = sum(results) / len(results)
    support_fraction = sum(1 for r in results if any(x >= math.log(n) for x, n in zip([r], [n_values[0]]))) / len(results)
    
    if all(r >= math.log(n) for r, n in zip(results, n_values)) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={math.sqrt(sum((x - mean_variance) ** 2 for x in results) / len(results))} support_fraction={support_fraction}")
    elif any(r < math.log(n) for r, n in zip(results, n_values)):
        first_failing_seed = seeds[results.index(min([r for r in results if r < math.log(n)]))]
        print(f"RESULT: FALSIFIED counterexample=\"variance_less_than_log_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")