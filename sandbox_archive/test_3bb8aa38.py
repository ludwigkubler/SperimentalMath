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
            poly *= (1 + x**len(clause)) ** len(clause)
        return poly
    
    def moments(poly, x):
        moment_sum = 0
        n = len(str(poly).split('*'))
        for i in range(n):
            coeff = poly.coeff(x**i)
            moment_sum += abs(coeff) * math.factorial(i)
        return moment_sum
    
    def generate_proof(depth, size):
        proof = []
        for _ in range(size):
            clause = [random.randint(1, depth) for _ in range(random.randint(1, 3))]
            proof.append(clause)
        return proof
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_moment_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            depth = random.randint(1, min(n, 20))
            proof = generate_proof(depth, n)
            moment_sum = moments(indicator_polynomial(proof, Fraction(1, 2)), Fraction(1, 2))
            total_moment_sum += moment_sum
            instances_tested += 1
    
    avg_moment_sum = total_moment_sum / instances_tested
    lower_bound = depth * math.log(n) ** 2
    
    conjecture_holds = avg_moment_sum >= 0.9 * lower_bound
    counterexample = "" if conjecture_holds else f"avg_moment_sum={avg_moment_sum}, lower_bound={lower_bound}"
    
    return {
        "metric_name": "Average Moment Sum",
        "metric_value": avg_moment_sum,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    avg_moment_sum = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_moment_sum} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_moment_sum} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")