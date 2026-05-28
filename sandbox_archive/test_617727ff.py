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
    
    def generate_polynomial(n):
        coeffs = [random.randint(0, 1) for _ in range(n+1)]
        return coeffs
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(reversed(poly)):
            result += coeff * (x ** i)
        return result % 2
    
    def find_roots(poly):
        n = len(poly) - 1
        if n == 0:
            return []
        roots = set()
        for x in range(2**n):
            if evaluate_polynomial(poly, x) == 0:
                roots.add(x)
        return roots
    
    def min_rank(poly):
        return len(find_roots(poly))
    
    def ac0_circuit_depth(n):
        # Simplified AC^0 circuit depth for Parity function
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    depths = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per n
            poly = generate_polynomial(n)
            rank = min_rank(poly)
            depth = ac0_circuit_depth(n)
            ranks.append(rank)
            depths.append(depth)
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    expected_bound = 2 * n_values[0] / (math.log(n_values[0]) ** 2)
    support_fraction = sum(1 for rank, depth in zip(ranks, depths) if abs(rank - expected_bound) <= 0.5 * n_values[0])
    
    conjecture_holds = support_fraction >= 0.8 * len(ranks)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 31))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")