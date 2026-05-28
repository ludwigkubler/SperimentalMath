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
    
    def multivariate_generalized_polynomial(f, n):
        # Simplified representation using a dictionary
        poly = {}
        for i in range(len(f)):
            term = []
            for j in range(n):
                if (i >> j) & 1:
                    term.append(f'x{j}')
                else:
                    term.append('~x{j}')
            poly[''.join(term)] = f[i]
        return poly
    
    def frege_proof_depth(poly, n):
        # Simplified estimation of Frege proof depth
        max_depth = 0
        for term in poly:
            depth = len(term.split('x')) - 1
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    def min_rank(poly):
        # Simplified calculation of minimal rank (number of terms)
        return len(poly)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    poly = multivariate_generalized_polynomial(f, n)
    depth = frege_proof_depth(poly, n)
    rank = min_rank(poly)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= depth,
        "counterexample": "" if rank <= depth else f"Rank {rank} > Depth {depth}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank > Depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")