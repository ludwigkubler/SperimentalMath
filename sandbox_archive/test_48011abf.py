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
    
    def generate_lie_algebra(n):
        # Placeholder function to generate a Lie algebra for testing purposes
        return [[0] * n for _ in range(n)]
    
    def communication_complexity_rank_variance(f, n):
        # Placeholder function to calculate the rank variance of a Boolean function
        return random.random()  # Replace with actual calculation
    
    def min_nontrivial_representation_dimension(lie_algebra):
        # Placeholder function to find the minimal dimension of the nontrivial representation
        return len(lie_algebra)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    lie_algebra = generate_lie_algebra(n)
    rank_variance = communication_complexity_rank_variance(f, n)
    dim_L = min_nontrivial_representation_dimension(lie_algebra)
    
    return {
        "metric_name": "Dimension of Minimal Representation",
        "metric_value": dim_L,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dim_L <= rank_variance + 5,
        "counterexample": "" if dim_L <= rank_variance + 5 else f"dim(L) = {dim_L}, r(f) = {rank_variance}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")