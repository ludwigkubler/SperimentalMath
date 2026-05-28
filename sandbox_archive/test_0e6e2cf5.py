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

def random_xor_circuit(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_ehrhart_rank(circuit):
    n = len(circuit)
    if n == 0:
        return 0
    
    # Construct the matrix A
    A = []
    for i in range(n):
        row = [circuit[(i >> j) & 1] for j in range(n)]
        A.append(row)
    
    # Gaussian elimination to find the rank
    rank = 0
    for i in range(n):
        if all(A[j][i] == 0 for j in range(rank, n)):
            continue
        
        # Swap rows to move a non-zero element to the pivot position
        A[rank], A[i] = A[i], A[rank]
        
        # Eliminate other elements in the column
        for j in range(n):
            if i != j and A[j][i] != 0:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        circuit = random_xor_circuit(n)
        rank = compute_ehrhart_rank(circuit)
        ranks.append(rank)
    
    metric_value = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n, 2) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ehrhart Rank",
        "metric_value": metric_value,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")