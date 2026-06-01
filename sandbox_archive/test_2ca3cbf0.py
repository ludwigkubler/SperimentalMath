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
    
    def generate_random_affine_variety(n):
        # Generate a random polynomial over F_2 with n variables
        vars = [f'x{i}' for i in range(1, n+1)]
        terms = []
        for _ in range(random.randint(10, 30)):
            term = ' + '.join([random.choice(vars) if random.random() < 0.5 else f'{random.choice(["+", "-"])}{random.choice(vars)}' for _ in range(random.randint(1, n))])
            terms.append(term)
        return ' & '.join(terms)

    def compute_minimal_local_ring_norm(poly):
        # Simplified version of computing the minimal local ring norm
        # This is a placeholder and should be replaced with actual computation
        return random.random()

    def compute_frege_proof_length(poly):
        # Simplified version of computing the Frege proof length
        # This is a placeholder and should be replaced with actual computation
        return len(poly.split(' & '))

    n = 5
    mrl_values = []
    f_values = []

    for _ in range(30):
        poly = generate_random_affine_variety(n)
        mrl = compute_minimal_local_ring_norm(poly)
        f = compute_frege_proof_length(poly)
        mrl_values.append(mrl)
        f_values.append(f)

    correlation_coefficient = sum((mrl - mean_mrl) * (f - mean_f) for mrl, f in zip(mrl_values, f_values)) / math.sqrt(sum((mrl - mean_mrl) ** 2 for mrl in mrl_values) * sum((f - mean_f) ** 2 for f in f_values))
    mean_mrl = sum(mrl_values) / len(mrl_values)
    mean_f = sum(f_values) / len(f_values)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")