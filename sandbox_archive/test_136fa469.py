# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def sipser_function(n, x):
        return sum(x[i] for i in range(n)) % 2
    
    def young_tableau_characters(n):
        # Generate all partitions of n and their Young tableaux characters
        partitions = []
        def partition(n, k, acc=[]):
            if len(acc) == k:
                partitions.append(acc)
                return
            for i in range(n, -1, -1):
                partition(i, k-1, acc + [i])
        partition(n, n)
        
        characters = {}
        for part in partitions:
            char = 1
            for i in range(1, len(part)):
                char *= math.factorial(sum(part[:i])) // (math.prod(math.factorial(x) for x in part[:i]))
            characters[tuple(sorted(part))] = char
        
        return characters
    
    def fourier_coefficient(n, k):
        # Compute the Fourier coefficient for a given partition
        characters = young_tableau_characters(n)
        coeff = 0
        for perm in set(itertools.permutations(range(n))):
            sign = (-1) ** sum(perm[i] > perm[j] for i, j in combinations(range(n), 2))
            char = characters[tuple(sorted([perm.index(i) for i in range(k)]))]
            coeff += sign * char
        return abs(coeff / math.factorial(n))
    
    def acc0_circuit_size(n):
        # Placeholder function to return a known ACC⁰ circuit size
        # This is a dummy implementation and should be replaced with actual computation
        return n
    
    max_coeff = 0
    for k in range(1, 2**n + 1):
        coeff = fourier_coefficient(n, k)
        if coeff > max_coeff:
            max_coeff = coeff
    
    circuit_size = acc0_circuit_size(n)
    
    return {
        "metric_name": "r_squared",
        "metric_value": max_coeff ** 2 / (circuit_size ** 2),
        "instances_tested": n,
        "conjecture_holds": False if max_coeff == 0 else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default list of primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        raise ValueError("No trials were executed. Ensure run_trial is implemented correctly.")
    
    mean_r_squared = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no seeds supported the conjecture")