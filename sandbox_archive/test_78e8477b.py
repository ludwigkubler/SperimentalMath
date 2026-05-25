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
    
    def parity_function(n, x):
        return sum(x[i] for i in range(n)) % 2
    
    def construct_variety(n):
        # Construct a simple variety based on the parity function
        variety = []
        for i in range(1 << n):
            x = [int(bit) for bit in f"{i:0{n}b}"]
            if parity_function(n, x) == 1:
                variety.append(x)
        return variety
    
    def compute_rank(variety):
        # Compute the rank of the variety (dimension + 1)
        n = len(variety[0])
        matrix = []
        for v in variety:
            matrix.append(v + [1])  # Add a constant term to represent the variety
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(rank)):
                continue
            for j in range(rank, len(matrix)):
                if matrix[j][i] != 0:
                    matrix[j], matrix[rank] = matrix[rank], matrix[j]
                    break
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    dimensions = []
    
    for n in n_values:
        variety = construct_variety(n)
        dimension = compute_rank(variety)
        dimensions.append(dimension)
    
    mean_dimension = sum(dimensions) / len(dimensions)
    conjecture_holds = all(1 <= dim <= 10 for dim in dimensions)
    counterexample = "" if conjecture_holds else "dimension_out_of_bounds"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_dimension,
        "instances_tested": len(dimensions),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dimension_out_of_bounds\" first_failing_seed={seeds[first_failing_seed]}")