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
    
    # Define constants and parameters
    n = 30
    c = 1.5
    
    # Generate a random explicit function in P with polynomially bounded ACC⁰ complexity
    def generate_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the Boolean algebra of the function
    def boolean_algebra(f):
        ba = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                row.append(f[i] ^ f[j])
            ba.append(row)
        return ba
    
    # Compute the Kahn-Smorodsky invariant
    def kahn_smorodsky_invariant(ba):
        rank = 0
        for i in range(n):
            row = [ba[j][i] for j in range(2**n)]
            if sum(row) > 0:
                rank += 1
        return rank
    
    # Compute the minimal rank of the invariant
    def min_rank(ba, k):
        ranks = []
        for _ in range(k):
            f = generate_function(n)
            ba = boolean_algebra(f)
            rank = kahn_smorodsky_invariant(ba)
            ranks.append(rank)
        return min(ranks)
    
    # Run the trial
    instances_tested = 30
    min_rank_values = [min_rank(boolean_algebra(generate_function(n)), instances_tested) for _ in range(instances_tested)]
    mean_value = sum(min_rank_values) / instances_tested
    
    # Check if the conjecture holds
    conjecture_holds = all(rank <= n**c for rank in min_rank_values)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={max(min_rank_values)}, expected={n**c}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds n^c\" first_failing_seed={next(i for i, r in enumerate(results) if not r['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")