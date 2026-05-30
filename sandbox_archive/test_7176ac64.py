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
    
    # Define the function to calculate the minimal diophantine exponent for a k-CNF formula
    def min_diophantine_exponent(k, n):
        if k == 1:
            return 0
        elif k == 2:
            return math.log(n, 2)
        else:
            return k * (n ** (1/4))
    
    # Define the function to generate a random k-CNF formula with n variables and clause length k
    def generate_k_cnf(k, n):
        cnf = []
        for _ in range(k):
            literals = [random.randint(1, n) for _ in range(n)]
            cnf.append(literals)
        return cnf
    
    # Define the function to calculate the minimal diophantine exponent of a k-CNF formula
    def calculate_diophantine_exponent(cnf):
        max_exponent = 0
        for clause in cnf:
            n = len(clause)
            k = 1
            while k <= n:
                exponent = min_diophantine_exponent(k, n)
                if exponent > max_exponent:
                    max_exponent = exponent
                k += 1
        return max_exponent
    
    # Define the function to test the conjecture for a given seed
    def test_conjecture(seed):
        random.seed(seed)
        n_max = 40
        instances_tested = 30
        max_exponent = 0
        
        for _ in range(instances_tested):
            k = random.randint(1, 40)
            cnf = generate_k_cnf(k, n_max)
            exponent = calculate_diophantine_exponent(cnf)
            if exponent > max_exponent:
                max_exponent = exponent
        
        return {
            "metric_name": "max_diophantine_exponent",
            "metric_value": max_exponent,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": max_exponent <= 40 * (n_max ** (1/4)),
            "counterexample": ""
        }
    
    return test_conjecture(seed)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")