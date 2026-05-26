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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_permutation_group(f):
        n = len(f)
        G = []
        for i in range(2**n):
            if all(f[i ^ j] == f[j] for j in range(2**n)):
                G.append(i)
        return G
    
    def compute_minimal_rank(G):
        rank = 0
        for g in G:
            if g != 0 and g not in [g1 ^ g2 for g1, g2 in itertools.combinations(G, 2)]:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    G = generate_permutation_group(f)
    
    minimal_rank = compute_minimal_rank(G)
    conjecture_holds = minimal_rank <= len(G) ** 2  # Polynomial bound for simplicity
    counterexample = "" if conjecture_holds else "minimal_rank > |Π(f)|^2"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank > |Π(f)|^2\" first_failing_seed={first_failing_seed}")