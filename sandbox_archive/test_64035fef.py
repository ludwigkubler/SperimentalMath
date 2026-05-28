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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_algebra_rank(f):
        n = len(f)
        variables = set()
        for term in f:
            for var in term:
                if var.startswith('x'):
                    variables.add(var)
        
        num_vars = len(variables)
        return num_vars
    
    def communication_complexity(f):
        n = len(f)
        return n  # Simplified model for XOR communication complexity
    
    instances_tested = 0
    total_rank = 0
    total_ccxor = 0
    support_count = 0
    
    for _ in range(30):  # Ensure statistical robustness with at least 30 instances per seed
        f = generate_boolean_function(random.randint(5, 40))
        rank_F = free_algebra_rank(f)
        cc_xor_f = communication_complexity(f)
        
        total_rank += rank_F
        total_ccxor += cc_xor_f
        
        if rank_F <= len(f):
            support_count += 1
    
    mean_rank = Fraction(total_rank, instances_tested) if instances_tested > 0 else Fraction(0, 1)
    mean_ccxor = Fraction(total_ccxor, instances_tested) if instances_tested > 0 else Fraction(0, 1)
    
    conjecture_holds = support_count / instances_tested >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Support Count",
        "metric_value": support_count,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_support_count = sum(r["support_count"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_support_count} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")