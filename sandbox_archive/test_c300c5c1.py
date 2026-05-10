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
    
    def generate_3cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def hook_length_formula(shape):
        n = len(shape)
        total = 1
        for i in range(n):
            for j in range(i + 1):
                total *= (shape[i] - j) * (n - i - j)
        for i in range(1, n):
            for j in range(i):
                total //= (i - j) * (j + 1)
        return math.factorial(n) // total
    
    def count_syt(shape):
        m = len(shape)
        if shape == [3] * m:
            cnf = generate_3cnf(m, m)
            # Count SYT for permanent shape
            syt_count = 0
            for perm in itertools.permutations(range(1, m + 1)):
                valid = True
                for i in range(m):
                    if (perm[i] % 3 == 0 and perm[(i + 1) % m] % 3 != 0) or \
                       (perm[i] % 3 == 1 and perm[(i + 2) % m] % 3 != 0) or \
                       (perm[i] % 3 == 2 and perm[(i + 4) % m] % 3 != 0):
                        valid = False
                        break
                if valid:
                    syt_count += 1
            return syt_count
        else:
            # Count SYT for determinant shape
            n = len(shape)
            total = 0
            for perm in itertools.permutations(range(1, n + 1)):
                valid = True
                for i in range(n):
                    if (perm[i] % n == 0 and perm[(i + 1) % n] % n != 0) or \
                       (perm[i] % n == 1 and perm[(i + 2) % n] % n != 0) or \
                       (perm[i] % n == 2 and perm[(i + 3) % n] % n != 0):
                        valid = False
                        break
                if valid:
                    total += 1
            return total
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = n // 3
        permanent_shape = [3] * m
        determinant_shape = list(range(n, 0, -1))
        
        permanent_syt_count = count_syt(permanent_shape)
        determinant_syt_count = count_syt(determinant_shape)
        
        ratio = permanent_syt_count / (2 ** (n ** 2 / 4) * determinant_syt_count)
        
        results.append({
            "metric_name": "SYT Count Ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": ratio >= 1,
            "counterexample": "" if ratio >= 1 else f"3-CNF with n={n}, m={m} violates the conjecture"
        })
    
    return {
        "metric_name": "SYT Count Ratio",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")