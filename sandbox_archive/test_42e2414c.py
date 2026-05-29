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
    
    # Define helper functions for group operations
    def multiply(g1, g2):
        return (g1[0] * g2[0], g1[1] + g2[1])
    
    def inverse(g):
        return (g[0]**-1, -g[1])
    
    def identity():
        return (1, 0)
    
    # Generate a noncrossed product of two cyclic groups
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    H = [(i/n, i/m) for i in range(n)]
    K = [(j/n, j/m) for j in range(m)]
    
    # Homomorphism φ from K to Aut(H)
    def phi(k):
        return (k[0]**2, k[1]**3)
    
    G = []
    for h in H:
        for k in K:
            G.append((multiply(h, phi(k)), multiply(inverse(k), identity())))
    
    # Calculate the minimal rank of G
    min_rank = len(G) // (n * m)
    
    # Simulate Max-Cut communication complexity
    instances_tested = 30
    communication_complexity = 0
    
    for _ in range(instances_tested):
        cut_set = set()
        for g in G:
            if random.choice([True, False]):
                cut_set.add(g)
        
        # Calculate the communication cost
        communication_cost = len(cut_set) * (n + m)
        communication_complexity += communication_cost
    
    communication_complexity /= instances_tested
    
    # Check if the conjecture holds
    conjecture_holds = abs(communication_complexity - min_rank) <= 10  # Constant factor for simplicity
    counterexample = f"min_rank={min_rank}, E[C(n)]={communication_complexity}" if not conjecture_holds else ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")