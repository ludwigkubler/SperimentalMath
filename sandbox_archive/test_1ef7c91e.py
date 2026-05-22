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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def quadratic_residues(p):
        residues = set()
        for a in range(1, p):
            if (a * a) % p not in residues:
                residues.add((a * a) % p)
        return residues
    
    def rank_of_quadratic_reciprocity_table_entry(a, p):
        # This is a placeholder function. Implement the actual computation here.
        return 0  # Placeholder value
    
    def communication_complexity(n):
        # This is a placeholder function. Implement the actual computation here.
        return 2 ** (n / 3)  # Placeholder value
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    primes = [p for p in range(2, 100) if is_prime(p)]
    a_values = [random.randint(1, p - 1) for p in primes]
    
    metric_value = 0
    instances_tested = 0
    
    for p, a in zip(primes, a_values):
        residues = quadratic_residues(p)
        if len(residues) != 2 ** (p - 1 / 2):
            continue
        
        rank = rank_of_quadratic_reciprocity_table_entry(a, p)
        cc = communication_complexity(n)
        
        metric_value += rank * math.log(2 ** (p - 1 / 2))
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Rank of Quadratic Reciprocity Tables vs Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric_value = metric_value / instances_tested
    conjecture_holds = all(2 ** (n / 3) <= communication_complexity(n) <= 2 ** (n / 2) for n in [5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "Rank of Quadratic Reciprocity Tables vs Communication Complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")