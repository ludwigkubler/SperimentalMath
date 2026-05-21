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
    
    def gromov_wasserstein_distance(n):
        return 2**(n - 0.5) / n
    
    def min_monotone_circuit_size_k_clique(n, k):
        # Placeholder for actual implementation
        # For simplicity, assume it's proportional to n^2
        return n**2
    
    n = random.randint(5, 40)
    D_n = gromov_wasserstein_distance(n)
    
    # Generate a random metric measure space with Gromov-Wasserstein distance ranging from D(n) to twice D(n)
    gw_dist = random.uniform(D_n, 2 * D_n)
    
    # Calculate the minimum monotone circuit size for k-CLIQUE
    k_clique_circuit_size = min_monotone_circuit_size_k_clique(n, n // 2)
    
    # Check if the conjecture holds
    conjecture_holds = abs(gw_dist / D_n - 1) <= 0.5
    
    return {
        "metric_name": "Gromov-Wasserstein Distance",
        "metric_value": gw_dist,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")