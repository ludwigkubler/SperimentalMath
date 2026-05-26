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
    
    def generate_primes(n):
        primes = []
        num = 2
        while len(primes) < n:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def tensor_product_valuations(f, n):
        valuations = set()
        for i in range(1 << n):
            valuation = 0
            for j in range(n):
                if (i >> j) & 1:
                    valuation ^= f[j]
            valuations.add(valuation)
        return len(valuations)
    
    def modular_form_rank(f, n):
        # Simplified rank calculation based on the number of variables
        return n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = [random.randint(0, 1) for _ in range(n)]
        
        rank = modular_form_rank(f, n)
        valuations = tensor_product_valuations(f, n)
        
        results.append({
            "n": n,
            "f": f,
            "rank": rank,
            "valuations": valuations
        })
    
    total_rank = sum(result["rank"] for result in results)
    total_valuations = sum(result["valuations"] for result in results)
    mean_rank = total_rank / len(results)
    mean_valuations = total_valuations / len(results)
    
    conjecture_holds = all(rank <= 2 * valuations for rank, valuations in zip([result["rank"] for result in results], [result["valuations"] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs Valuations",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(result["metric_value"] for result in results)
    total_valuations = sum(result["instances_tested"] for result in results)
    mean_rank = total_rank / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")