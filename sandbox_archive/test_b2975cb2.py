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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def generate_symmetric_block_design(v, k, lambd):
    if v < k or k < lambd or v % k != 0:
        raise ValueError("Invalid parameters for symmetric block design")
    
    blocks = []
    points = list(range(v))
    for i in range(k):
        block = random.sample(points, k)
        blocks.append(block)
    
    # Ensure all pairs of blocks intersect exactly lambda times
    while True:
        valid = True
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                if len(set(blocks[i]) & set(blocks[j])) != lambd:
                    valid = False
                    break
            if not valid:
                break
        
        if valid:
            break
    
    return blocks

def construct_communication_matrix(blocks):
    v = len(blocks[0])
    n = len(blocks)
    matrix = [[0] * n for _ in range(v)]
    
    for i, block in enumerate(blocks):
        for point in block:
            matrix[point][i] = 1
    
    return matrix

def compute_discrepancy(matrix):
    v, n = len(matrix), len(matrix[0])
    max_discrepancy = 0
    
    for i in range(v):
        for j in range(n):
            row_sum = sum(matrix[i])
            col_sum = sum(matrix[k][j] for k in range(v))
            discrepancy = abs(row_sum - col_sum)
            if discrepancy > max_discrepancy:
                max_discrepancy = discrepancy
    
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(n_tests):
        v = random.choice([5, 10, 15, 20, 30, 40])
        k = random.randint(2, v // 2)
        lambd = random.randint(1, k - 1)
        
        try:
            blocks = generate_symmetric_block_design(v, k, lambd)
            matrix = construct_communication_matrix(blocks)
            discrepancy = compute_discrepancy(matrix)
            
            expected_bound = math.sqrt(lambd * v / k)
            if discrepancy < expected_bound:
                conjecture_holds = False
                counterexample = f"v={v}, k={k}, λ={lambd}"
                break
            
            total_metric_value += discrepancy
            instances_tested += 1
        except ValueError as e:
            conjecture_holds = False
            counterexample = str(e)
            break
    
    return {
        "metric_name": "discrepancy",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")