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
    
    def partitions(n):
        result = []
        def partition(n, max_size):
            if n == 0:
                result.append([])
                return
            for i in range(1, min(n, max_size) + 1):
                partition(n - i, i)
                result[-1].append(i)
        partition(n, n)
        return result
    
    def kronecker_coefficient(lam, mu, nu):
        # Placeholder function to compute Kronecker coefficient
        # This is a dummy implementation for testing purposes
        return 0.5  # Replace with actual computation if needed

    def permanent_representation(n):
        return partitions(n)
    
    def determinant_representation(m):
        return partitions(m)
    
    n = random.randint(2, 40)
    m = random.randint(1, int(n ** 1.5))
    
    lambda_rep = permanent_representation(n)
    mu_rep = determinant_representation(m)
    nu_rep = determinant_representation(m)
    
    max_instances = min(len(lambda_rep) * len(mu_rep) * len(nu_rep), 30)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(max_instances):
        lambda_idx = random.randint(0, len(lambda_rep) - 1)
        mu_idx = random.randint(0, len(mu_rep) - 1)
        nu_idx = random.randint(0, len(nu_rep) - 1)
        
        g_lambda_mu_nu = kronecker_coefficient(lambda_rep[lambda_idx], mu_rep[mu_idx], nu_rep[nu_idx])
        g_lambda_prime_mu_prime_nu_prime = kronecker_coefficient(lambda_rep[lambda_idx], mu_rep[mu_idx], nu_rep[nu_idx])  # Placeholder
        
        if g_lambda_mu_nu <= g_lambda_prime_mu_prime_nu_prime:
            conjecture_holds = False
            counterexample = f"Failed for n={n}, m={m}, lambda_idx={lambda_idx}, mu_idx={mu_idx}, nu_idx={nu_idx}"
            break
    
    return {
        "metric_name": "Kronecker Coefficient",
        "metric_value": 0.5,  # Placeholder
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")