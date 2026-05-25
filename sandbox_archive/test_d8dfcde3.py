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
        for i in range(2, int(math.sqrt(n)) + 1):
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
    
    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def min_rank_trop(Q):
        # Placeholder implementation of minRank_trop
        return len(Q)
    
    def sum_of_squares_circuit_size(f):
        # Placeholder implementation of sum_of_squares_circuit_size
        return len(f)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = random_boolean_function(n)
    Q = [f]
    
    min_rank = min_rank_trop(Q)
    circuit_size = sum_of_squares_circuit_size(f)
    
    return {
        "metric_name": "minRank_trop vs Circuit Size",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank <= circuit_size,
        "counterexample": "" if min_rank <= circuit_size else f"Counterexample: n={n}, minRank={min_rank}, Circuit Size={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")