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
    
    def generate_primes(limit):
        primes = []
        for num in range(2, limit):
            if is_prime(num):
                primes.append(num)
        return primes
    
    def generate_random_3sat_instance(n):
        clauses = []
        for _ in range(3 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def gf2_polynomial_from_3sat(clauses):
        n = max(abs(var) for clause in clauses for var in clause)
        poly = [0] * (1 << n)
        for clause in clauses:
            product = 1
            for var in clause:
                if var > 0:
                    product ^= 1 << (var - 1)
                else:
                    product ^= 1 << (-var - 1)
            poly[product] += 1
        return poly
    
    def factorize_poly(poly):
        n = len(poly)
        factors = []
        for i in range(1, n):
            if poly[i] != 0 and all(poly[j] % poly[i] == 0 for j in range(i + 1, n)):
                factors.append([i])
                break
        return factors
    
    def count_irreducible_components(poly):
        return len(factorize_poly(poly))
    
    def acc0_circuit_size_estimate(n):
        return 2 ** (n // 2)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_random_3sat_instance(n)
    poly = gf2_polynomial_from_3sat(instance)
    irreducible_components_count = count_irreducible_components(poly)
    acc0_size_estimate = acc0_circuit_size_estimate(n)
    
    return {
        "metric_name": "irreducible_components_count",
        "metric_value": irreducible_components_count,
        "instances_tested": 1,
        "conjecture_holds": irreducible_components_count >= acc0_size_estimate,
        "counterexample": "" if irreducible_components_count >= acc0_size_estimate else f"n={n}, poly={poly}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(100)[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")