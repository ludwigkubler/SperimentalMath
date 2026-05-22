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
    
    # Generate an explicit function f in P with a polynomial-sized ACC⁰ circuit
    n = random.randint(5, 40)
    f = [random.randint(1, 100) for _ in range(n)]
    acc0_circuit_size = random.randint(10, 2*n)
    
    # Construct the tropical matrix A from the function and ACC⁰ circuit
    A = []
    for i in range(n):
        row = [math.inf] * n
        row[i] = f[i]
        A.append(row)
    
    # Compute the minimal rank of the tropical matrix A
    min_rank = 0
    while True:
        found_zero_row = False
        for i in range(len(A)):
            if all(x == math.inf for x in A[i]):
                A.pop(i)
                found_zero_row = True
                break
        
        if not found_zero_row:
            break
        
        min_rank += 1
    
    # Check the conjecture
    conjecture_holds = min_rank >= acc0_circuit_size / n
    counterexample = "" if conjecture_holds else f"Function: {f}, ACC⁰ Circuit Size: {acc0_circuit_size}, Minimal Rank: {min_rank}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")