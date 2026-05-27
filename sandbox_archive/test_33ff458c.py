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
    
    def generate_explicit_function(n):
        # Placeholder for generating an explicit function with known ACC⁰ lower bound
        return [random.randint(1, n) for _ in range(n)]
    
    def calculate_fourier_coefficients(f):
        # Placeholder for calculating Fourier coefficients of a function
        return [sum(f[i] * math.exp(-2j * math.pi * i * k / len(f)) for i in range(len(f))) / len(f) for k in range(len(f))]
    
    def eichler_shimura_relations(fourier_coeffs):
        # Placeholder for calculating Eichler-Shimura relations
        return [sum(fourier_coeffs[i] * fourier_coeffs[j] for i in range(len(fourier_coeffs)) for j in range(i+1, len(fourier_coeffs))) for _ in range(len(fourier_coeffs))]
    
    def minimal_rank(relations):
        # Placeholder for calculating the minimal rank of a matrix
        return sum(1 for row in relations if any(row[i] != 0 for i in range(len(row))))
    
    n = random.randint(5, 40)
    f = generate_explicit_function(n)
    fourier_coeffs = calculate_fourier_coefficients(f)
    relations = eichler_shimura_relations(fourier_coeffs)
    min_rank_value = minimal_rank(relations)
    
    c = 1.0  # Placeholder for the constant in O(log^c(n))
    expected_bound = Fraction(n).log2().limit_denominator() ** c
    
    conjecture_holds = abs(min_rank_value - expected_bound) <= 3
    counterexample = f"min_rank={min_rank_value}, expected_bound={expected_bound}" if not conjecture_holds else ""
    
    return {
        "metric_name": "MinimalRank",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(res["metric_value"] - expected_bound) > 3 or res["metric_value"] > 10 for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results, start=seeds[0]) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=min_rank={min_rank_value}, expected_bound={expected_bound} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")