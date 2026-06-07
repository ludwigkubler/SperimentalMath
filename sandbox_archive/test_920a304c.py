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
    
    # Generate a random d-regular graph with n variables (n ≤ 40)
    n = random.randint(5, 30)
    d = random.randint(2, min(n - 1, 3))
    edges = set()
    for i in range(n):
        neighbors = random.sample(range(n), d)
        for j in neighbors:
            if i < j and (i, j) not in edges and (j, i) not in edges:
                edges.add((i, j))
    
    # Construct the geometric object corresponding to φ_G
    # This is a placeholder function. Replace with actual implementation.
    def construct_geometric_object(graph):
        return graph
    
    geometric_object = construct_geometric_object(edges)
    
    # Calculate the minimal symplectic invariant msi(G) of this geometric object
    # This is a placeholder function. Replace with actual implementation.
    def calculate_msi(geometric_object):
        return random.random()  # Placeholder value
    
    msi_G = calculate_msi(geometric_object)
    
    # Measure the resolution proof width w(φ_G)
    # This is a placeholder function. Replace with actual implementation.
    def measure_resolution_width(phi_G):
        return random.randint(1, 10)  # Placeholder value
    
    phi_G = "Tseitin_formula"  # Placeholder value
    w_phi_G = measure_resolution_width(phi_G)
    
    # Correlate msi(G) with w(φ_G) using Pearson's correlation coefficient
    # This is a placeholder function. Replace with actual implementation.
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        if std_dev_x == 0 or std_dev_y == 0:
            return None
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation_coefficient = pearson_correlation([msi_G], [w_phi_G])
    
    # Determine if the conjecture holds for this seed
    conjecture_holds = correlation_coefficient is not None and abs(correlation_coefficient) >= 0.8
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")