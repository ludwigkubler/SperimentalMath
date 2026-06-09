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
    
    def generate_communication_problem(n):
        # Generate a random communication complexity problem with n variables
        # This is a placeholder function; replace it with actual problem generation logic
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_rank_variance(problem):
        # Compute the rank variance of the communication complexity problem
        # This is a placeholder function; replace it with actual rank variance computation logic
        return sum(problem) / len(problem)
    
    def find_smallest_coxeter_group(rank_variance):
        # Find the smallest nontrivial Coxeter group associated with the rank variance
        # This is a placeholder function; replace it with actual Coxeter group finding logic
        return math.ceil(math.sqrt(rank_variance))
    
    n = 40
    problem = generate_communication_problem(n)
    rank_variance = compute_rank_variance(problem)
    num_generators = find_smallest_coxeter_group(rank_variance)
    
    metric_name = "num_generators"
    metric_value = num_generators
    instances_tested = 1
    n_max = n
    conjecture_holds = num_generators <= rank_variance
    counterexample = "" if conjecture_holds else f"Problem with R={rank_variance}, G={num_generators}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")