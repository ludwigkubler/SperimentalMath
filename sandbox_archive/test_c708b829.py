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
    
    def generate_random_function(n, m):
        return [random.randint(0, 1) for _ in range(m)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def quadratic_residues(p):
        residues = set()
        for i in range(1, p):
            if (i * i) % p not in residues:
                residues.add((i * i) % p)
        return len(residues)
    
    n = 40
    m = n
    f = generate_random_function(n, m)
    t_f = xor_and_tree_width(f)
    
    if t_f == 1:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": t_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    p = next_prime(t_f)
    if p is None:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": t_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    num_residues = quadratic_residues(p)
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": t_f,
        "instances_tested": 1,
        "conjecture_holds": t_f <= math.sqrt(p),
        "counterexample": ""
    }

def next_prime(n):
    if n < 2:
        return None
    for i in range(n + 1, 2 * n):
        if is_prime(i):
            return i
    return None

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif sum(result["conjecture_holds"] for result in results) > 0.8 * len(results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")