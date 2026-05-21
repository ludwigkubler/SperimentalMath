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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def indicator_polynomial(proof, x):
        poly = 1
        for clause in proof:
            poly *= sum((1 + x**i)**k for i, k in clause.items())
        return poly
    
    def moments(poly, x):
        n = len(poly)
        moment_sum = 0
        for i in range(n):
            moment_sum += poly[i] * (x ** i)
        return moment_sum
    
    def generate_frege_proof(depth: int, size: int):
        proof = []
        for _ in range(size):
            clause = {}
            for _ in range(random.randint(1, depth)):
                var = random.randint(0, depth-1)
                if var not in clause:
                    clause[var] = 1
                else:
                    clause[var] += 1
            proof.append(clause)
        return proof
    
    def log_square(n):
        return n * math.log2(n) ** 2
    
    n_tests = 30
    total_moment_sum = 0
    min_moment_sum = float('inf')
    
    for _ in range(n_tests):
        depth = random.randint(5, 40)
        size = random.randint(1, depth)
        proof = generate_frege_proof(depth, size)
        moment_sum = moments(indicator_polynomial(proof, Fraction(1, 2)), Fraction(1, 2))
        total_moment_sum += moment_sum
        min_moment_sum = min(min_moment_sum, moment_sum)
    
    mean_moment_sum = total_moment_sum / n_tests
    support_fraction = (mean_moment_sum >= 0.9 * log_square(depth)) and (min_moment_sum >= 0.9 * log_square(depth))
    
    return {
        "metric_name": "moment_sum",
        "metric_value": mean_moment_sum,
        "instances_tested": n_tests,
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else f"Depth={depth}, Size={size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_moment_sum = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_moment_sum} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Depth={r['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")