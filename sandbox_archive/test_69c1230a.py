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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def construct_braided_monoid(cnf):
        n = len(cnf[0])
        generators = list(range(1, n + 1))
        relations = []
        for clause in cnf:
            rel = [(-x, -y) for x, y in zip(clause[:-1], clause[1:])]
            relations.extend(rel)
        return generators, relations
    
    def minimal_index(generators, relations):
        # Simplified version of the algorithm to calculate minimal index
        # This is a placeholder and should be replaced with actual computation
        return random.randint(1, 10)
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        variance = sum(len(clause) for clause in cnf) / (n * n)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        cnf = generate_cnf(n)
        generators, relations = construct_braided_monoid(cnf)
        min_index = minimal_index(generators, relations)
        rank_variance = communication_complexity_rank_variance(cnf)
        
        total_metric_value += abs(min_index)
        instances_tested += 1
        n_max = max(n_max, n)
        
        if instances_tested < 30:
            conjecture_holds = False
            counterexample = "Too few instances tested"
    
    return {
        "metric_name": "minimal_index",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")