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
    
    def generate_disjointness_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    def communication_matrix(A, B):
        n = len(A)
        C = [[A[i][j] & B[j][i] for j in range(n)] for i in range(n)]
        return C
    
    def additive_energy(C):
        n = len(C)
        count = 0
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    for l in range(k, n):
                        if C[i][j] + C[j][k] + C[k][l] + C[l][i] >= 3:
                            count += 1
        return count
    
    def discrepancy(C):
        n = len(C)
        max_cut = 0
        for i in range(n):
            for j in range(i, n):
                cut = sum(C[i][k] & C[j][k] for k in range(n))
                if cut > max_cut:
                    max_cut = cut
        return max_cut
    
    A, B = generate_disjointness_instance(5)
    C = communication_matrix(A, B)
    
    E = additive_energy(C)
    disc = discrepancy(C)
    
    metric_name = "additive_energy_over_disc"
    metric_value = E / disc if disc != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = abs(metric_value - 4) < 1e-6  # Assuming constant is close to 4 for n=5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in input().split()] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")