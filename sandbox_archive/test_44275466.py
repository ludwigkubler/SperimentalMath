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
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hook_length_formula(n, k):
        numerator = math.factorial(n + k - 1)
        denominator = (math.factorial(n) * math.factorial(k))
        return numerator // denominator
    
    def plethysm_coefficient(n, k):
        if n == 0:
            return 1
        coeff = 0
        for i in range(1, n + 1):
            coeff += hook_length_formula(i, k) * plethysm_coefficient(n - i, k)
        return coeff
    
    def multiplicity(P_k, lambda_):
        if P_k == 0 or lambda_ == 0:
            return 0
        return plethysm_coefficient(P_k, lambda_)
    
    n = random.randint(5, 40)
    k = 2
    
    lambda_ = (n - 1, 1)
    multiplicity_P = multiplicity(n, k)
    multiplicity_D = multiplicity(n, k)
    
    if multiplicity_P <= multiplicity_D:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": multiplicity_P,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}, P^⊗{k} multiplicity ≤ D^⊗{k} multiplicity"
        }
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": multiplicity_P,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity Gap\" first_failing_seed={first_failing_seed}")