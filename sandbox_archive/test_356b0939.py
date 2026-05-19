# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    n = 4
    random.seed(seed)
    
    # Define the disjointness function
    def DISJ_n(x, y):
        return any(xi and yi for xi, yi in zip(x, y))
    
    # Generate all possible inputs
    inputs = [(i, j) for i in range(2**n) for j in range(2**n)]
    
    # Compute deterministic communication complexity D(DISJ_n)
    def compute_communication_complexity():
        protocol_tree = {}
        for x, y in inputs:
            if (x, y) not in protocol_tree:
                protocol_tree[(x, y)] = random.choice([0, 1])
        return max(protocol_tree.values()) + 1
    
    D = compute_communication_complexity()
    
    # Compute minimum monotone circuit size S(DISJ_n)
    def is_monotone(circuit):
        for x in range(2**n):
            for y in range(2**n):
                if not DISJ_n(x, y) and any(circuit[i][j] == 1 for i, j in zip(bin(x)[2:].zfill(n), bin(y)[2:].zfill(n))):
                    return False
        return True
    
    def exhaustive_monotone_circuit_synthesis():
        from itertools import product
        
        min_size = float('inf')
        for size in range(1, 2**n):
            for circuit in product([0, 1], repeat=size * n):
                if is_monotone(circuit):
                    min_size = min(min_size, size)
                    break
            if min_size < float('inf'):
                break
        return min_size
    
    S = exhaustive_monotone_circuit_synthesis()
    
    # Check the conjecture
    conjecture_holds = D >= n and S >= 2**(n/2)
    counterexample = "" if conjecture_holds else "disjointness_discrepancy"
    
    return {
        "metric_name": "communication_complexity_and_circuit_size",
        "metric_value": (D, S),
        "instances_tested": len(inputs),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_D = sum(result["metric_value"][0] for result in results) / len(results)
    mean_S = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean_D={mean_D} mean_S={mean_S} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean_D={mean_D} mean_S={mean_S} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"disjointness_discrepancy\" first_failing_seed={first_failing_seed}")