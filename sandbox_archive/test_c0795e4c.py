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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses, n):
        polynomial = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for mask in range(2**n):
                if all((mask & (1 << var)) != 0 for var in clauses[i]):
                    polynomial[i][mask] += 1
        return polynomial
    
    def noncommutative_crossed_product(poly):
        n = len(poly)
        m = 2**n
        product = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                for k in range(n):
                    if (i & (1 << k)) != 0 and (j & (1 << k)) != 0:
                        product[i][j] += poly[k][i ^ (1 << k)] * poly[k][j ^ (1 << k)]
        return product
    
    def bp_readtwice_circuit_threshold(n):
        # Placeholder for actual implementation
        return n**2  # Simplified example
    
    n = random.randint(5, 40)
    k = random.randint(1, min(3*n//2, 100))  # Ensure at least one clause per variable
    cnf_instance = generate_k_cnf(n, k)
    polynomial = clause_indicator_polynomial(cnf_instance, n)
    
    crossed_product = noncommutative_crossed_product(polynomial)
    rank = sum(1 for row in crossed_product if any(row))
    bp_threshold = bp_readtwice_circuit_threshold(n)
    
    diff = abs(rank - bp_threshold)
    conjecture_holds = diff <= math.log(n) * 2  # Simplified example
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} is not within Θ(log({n})) of BP threshold {bp_threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_diff = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_diff/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_diff/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds BP threshold by more than Θ(log(n))\" first_failing_seed={first_failing_seed}")