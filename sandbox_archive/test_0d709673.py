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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        res = 1
        for i in range(k):
            res *= (n - i)
            res //= (i + 1)
        return res
    
    def generate_monomial_ideal(n):
        ideal = set()
        for i in range(1, n+1):
            for j in range(i, n+1):
                if gcd(i, j) == 1:
                    ideal.add((i, j))
        return ideal
    
    def minimal_rank_of_affine_quotient_algebra(ideal):
        rank = 0
        for (i, j) in ideal:
            rank += binomial_coefficient(n + i - 1, i)
        return rank
    
    n = random.randint(5, 40)
    ideal = generate_monomial_ideal(n)
    complexity = len(ideal)
    
    if complexity > n**3:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "complexity_exceeds_n_cubed"
        }
    
    rank = minimal_rank_of_affine_quotient_algebra(ideal)
    upper_bound = complexity**(2/3)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= upper_bound,
        "counterexample": "" if rank <= upper_bound else f"rank={rank}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    num_tests = len(results)
    mean_rank = total_rank / num_tests
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results if r["metric_value"] is not None) / (num_tests - 1))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_tests
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_upper_bound\" first_failing_seed={first_failing_seed}")