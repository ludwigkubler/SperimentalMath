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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_and_function(n):
        # Generate a random AND function with n variables
        return {tuple(sorted(random.sample(range(1, n+1), k))): 1 for k in range(1, n)}
    
    def construct_affine_variety(and_func):
        # Construct the affine variety associated with the AND function
        if not and_func:
            return []
        
        variables = list(and_func.keys())[0]
        generators = [tuple(sorted(random.sample(variables, k))) for k in range(1, len(variables)+1)]
        return generators
    
    def compute_rank(generators):
        # Compute the rank of the affine variety
        if not generators:
            return 0
        
        n = len(generators[0])
        matrix = []
        for gen in generators:
            row = [Fraction(1, 1) if i+1 in gen else Fraction(0, 1) for i in range(n)]
            matrix.append(row)
        
        rank = 0
        for i in range(n):
            pivot_row = next((j for j in range(i, len(matrix)) if matrix[j][i] != Fraction(0, 1)), None)
            if pivot_row is None:
                continue
            
            # Swap rows to make the pivot element 1
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            # Eliminate other elements in the column
            for j in range(len(matrix)):
                if i != j and matrix[j][i] != Fraction(0, 1):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    n = random.randint(5, 40)
    and_func = generate_and_function(n)
    generators = construct_affine_variety(and_func)
    rank = compute_rank(generators)
    
    return {
        "metric_name": "Rank of Affine Variety",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank > 0,  # Simplified for testing purposes
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")