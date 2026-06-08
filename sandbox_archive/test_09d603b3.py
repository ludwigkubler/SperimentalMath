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
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(n * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frobenius_class(cnf):
        primes = set()
        for clause in cnf:
            for lit in clause:
                if abs(lit) not in primes and is_prime(abs(lit)):
                    primes.add(abs(lit))
        return len(primes)
    
    def communication_complexity_rank_variance(truth_table):
        n = len(truth_table)
        rank_variances = []
        
        for _ in range(10):  # Sample multiple representations
            permuted_truth_table = truth_table[:]
            random.shuffle(permuted_truth_table)
            
            rank = 0
            for row in permuted_truth_table:
                if all(row[i] == 1 for i in range(n) if truth_table[i][0] > 0):
                    rank += 1
            rank_variances.append(rank)
        
        return sum((x - sum(rank_variances) / len(rank_variances)) ** 2 for x in rank_variances) / len(rank_variances)
    
    def truth_table_from_cnf(cnf):
        n = max(abs(lit) for lit in cnf)
        truth_table = [[0] * (n + 1) for _ in range(2**n)]
        
        for i, assignment in enumerate(itertools.product([0, 1], repeat=n)):
            for clause in cnf:
                if all(assignment[abs(lit) - 1] == 1 if lit > 0 else assignment[abs(lit) - 1] == 0 for lit in clause):
                    truth_table[i][0] = 1
                    break
        
        return truth_table
    
    def linear_function(n):
        return n * 2  # Example linear function, replace with actual C(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        frobenius_set_size = frobenius_class(cnf)
        truth_table = truth_table_from_cnf(cnf)
        rank_variance = communication_complexity_rank_variance(truth_table)
        
        if frobenius_set_size == 0 or rank_variance == 0:
            continue
        
        results.append((frobenius_set_size, linear_function(n) * rank_variance))
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    frobenius_values, rank_variance_values = zip(*results)
    correlation = sum((x - sum(frobenius_values) / len(frobenius_values)) * (y - sum(rank_variance_values) / len(rank_variance_values)) for x, y in zip(frobenius_values, rank_variance_values)) / (len(results) * sum((x - sum(frobenius_values) / len(frobenius_values)) ** 2 for x in frobenius_values))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.95 * sum(abs(x - sum(frobenius_values) / len(frobenius_values)) for x in frobenius_values) / len(frobenius_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.95 * std_dev) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")