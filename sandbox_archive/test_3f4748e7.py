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
    
    def generate_random_parity_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_rank(polynomial):
        n = len(polynomial)
        if n == 0:
            return 0
        rank = 0
        matrix = [[polynomial[i] ^ polynomial[j] for j in range(n)] for i in range(n)]
        for row in matrix:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
                for j in range(n):
                    if row[j] == 1:
                        for k in range(n):
                            matrix[k][j] ^= polynomial[k]
        return rank
    
    def tropicalize_polynomial(polynomial, p):
        n = len(polynomial)
        tropicalized = [0] * n
        for i in range(n):
            if polynomial[i] == 1:
                tropicalized[i] = math.log2(i + 1) / math.log2(p)
        return tropicalized
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit_size = 2**n
        if circuit_size > 2**(0.5 * n):
            continue
        polynomial = generate_random_parity_circuit(n)
        tropicalized_polynomial = tropicalize_polynomial(polynomial, 2)
        rank = compute_minimal_rank(tropicalized_polynomial)
        results.append((rank, circuit_size))
    
    if not results:
        return {
            "metric_name": "Minimal Rank vs Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_size = sum(size for _, size in results) / len(results)
    support_fraction = all(rank <= math.log2(size) for rank, size in results)
    
    return {
        "metric_name": "Minimal Rank vs Circuit Size",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")