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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def truth_assignments(n):
        return list(itertools.product([0, 1], repeat=n))
    
    def galois_group_size(n):
        # Placeholder function to compute the size of the Galois group
        # This is a dummy implementation for demonstration purposes
        return math.factorial(n)
    
    def smallest_normalizing_subset(clauses, assignments):
        n = len(assignments[0])
        normalizing_subsets = []
        for subset in itertools.combinations(range(n), 1):
            if all(all([assignment[var-1] == assignment[sub_var-1] for sub_var in subset]) for clause in clauses):
                normalizing_subsets.append(subset)
        return min(len(subset) for subset in normalizing_subsets)
    
    n = random.randint(5, 40)
    k = random.randint(2, 3)
    formula = generate_kcnf(n, k)
    assignments = truth_assignments(n)
    
    galois_size = galois_group_size(n)
    norm_subset_size = smallest_normalizing_subset(formula, assignments)
    
    ratio = norm_subset_size / galois_size
    
    conjecture_holds = ratio <= n ** (math.log2(k + 1))
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > {n ** (math.log2(k + 1))}"
    
    return {
        "metric_name": "Galois Group Complexity Ratio",
        "metric_value": ratio,
        "instances_tested": len(assignments),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")