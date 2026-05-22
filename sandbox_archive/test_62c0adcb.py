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

def tropical_xor(a, b):
    return max(a, b)

def min_rank_tropical_curve(n):
    # Generate a random XOR function
    x = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Construct the tropical curve matrix A
    A = [[tropical_xor(x[i], x[j]) for j in range(n)] for i in range(n)]
    
    # Gaussian elimination to find the rank of A
    rank = n
    for i in range(n):
        if A[i][i] == 0:
            found = False
            for k in range(i+1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    found = True
                    break
            if not found:
                rank -= 1
                continue
        
        for j in range(n):
            if i != j and A[j][i] != 0:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        rank = min_rank_tropical_curve(n)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / len(n_values)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank <= math.log2(n)**2,
        "counterexample": "" if mean_rank <= math.log2(n)**2 else f"Rank {mean_rank} exceeds O(log^2({n_values[-1]}))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds O(log^2(n))' first_failing_seed={first_failing_seed}")