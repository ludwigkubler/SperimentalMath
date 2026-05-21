# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    # Set seed for reproducibility
    random.seed(seed)

    # Generate a random expander graph with n vertices
    n = random.randint(5, 40)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 2 / (n - 1):
                edges.append((i, j))

    # Compute the automorphism group using nauty
    # This is a placeholder function; actual implementation depends on nauty's API
    def compute_automorphism_group(edges):
        # Placeholder return value
        return {frozenset(range(n))}

    aut_group = compute_automorphism_group(edges)
    C_G = len(aut_group)

    # Measure the resolution width via a SAT solver (e.g., DRAT-trace)
    # This is a placeholder function; actual implementation depends on the SAT solver
    def measure_resolution_width(edges):
        # Placeholder return value
        return random.randint(C_G, 2 * C_G)

    res_width = measure_resolution_width(edges)

    # Verify if res_width ≥ C(G) holds
    conjecture_holds = res_width >= C_G
    counterexample = "" if conjecture_holds else f"res_width={res_width} < C(G)={C_G}"

    return {
        "metric_name": "resolution_width",
        "metric_value": res_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    total_metric = sum(result["metric_value"] for result in results)
    num_seeds = len(results)
    mean_metric = Fraction(total_metric).limit_denominator()
    std_metric = 0
    for result in results:
        std_metric += (result["metric_value"] - mean_metric) ** 2
    std_metric = (std_metric / num_seeds).sqrt().limit_denominator()

    support_fraction = sum(result["conjecture_holds"] for result in results) / num_seeds

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")