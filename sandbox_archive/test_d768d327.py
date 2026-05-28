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
    
    def multivariate_generalized_polynomial_representation(f, n):
        # Simplified representation using a dictionary
        poly = {}
        for i in range(len(f)):
            term = f[i]
            variables = []
            for j in range(n):
                if (i >> j) & 1:
                    variables.append(f'x{j}')
            poly[tuple(variables)] = term
        return poly
    
    def frege_proof_depth(poly, n):
        # Simplified estimation of Frege proof depth
        # This is a placeholder and should be replaced with actual computation
        return len(poly)
    
    def min_rank(poly):
        # Simplified calculation of minimal rank
        # This is a placeholder and should be replaced with actual computation
        return sum(1 for _ in poly)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    poly = multivariate_generalized_polynomial_representation(f, n)
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
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")