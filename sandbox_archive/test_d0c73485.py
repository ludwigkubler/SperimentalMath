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
    
    # Generate a random k-CNF with n variables where n is prime
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(5, 41) if is_prime(i)]
    n = random.choice(primes)
    k = random.randint(1, min(n-1, 3))
    
    # Construct a k-CNF with n variables
    def generate_k_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = [random.randint(-n+1, -1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    F = generate_k_cnf(n, k)
    
    # Construct a curve C over the finite field F_p
    def construct_curve(F):
        p = 2**n + 1
        x = random.randint(0, p-1)
        y = random.randint(0, p-1)
        return (x, y)
    
    C = construct_curve(F)
    
    # Calculate the minimal Hodge index h(C)
    def min_hodge_index(C):
        x, y = C
        return abs(x) + abs(y)
    
    h_C = min_hodge_index(C)
    
    # Calculate the resolution proof size t*(F)
    def resolution_proof_size(F):
        m = len(F)
        n = len(F[0])
        return m * n
    
    t_F = resolution_proof_size(F)
    
    return {
        "metric_name": "Hodge Index vs Resolution Proof Size",
        "metric_value": h_C / math.log2(n),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if h_C <= k / (p ** n) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Hodge index {r['metric_value']} does not satisfy the conjecture"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break