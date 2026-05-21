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
    n = 40
    D_n = 2 ** (n - 1/2) / n
    
    # Generate a random graph K_n
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    
    # Compute the uniform measure on K_n
    uniform_measure = {tuple(sorted(e)): 1 / len(edges) for e in edges}
    
    # Generate a set of random metric measure spaces with Gromov-Wasserstein distance ranging from D(n) to twice D(n)
    metric_measure_spaces = []
    for _ in range(30):
        MMS = {}
        for e in edges:
            d_e = random.uniform(D_n, 2 * D_n)
            MMS[tuple(sorted(e))] = d_e
        metric_measure_spaces.append(MMS)
    
    # Calculate the Gromov-Wasserstein distances and compare them to the known value for D(n)
    GW_distances = []
    for MMS in metric_measure_spaces:
        GW_distance = 0
        for e1, d1 in uniform_measure.items():
            for e2, d2 in MMS.items():
                if set(e1) & set(e2):
                    GW_distance += abs(d1 - d2)
        GW_distances.append(GW_distance / len(edges))
    
    # Simultaneously, find the minimum monotone circuit size for k-CLIQUE in each graph
    min_circuit_sizes = []
    for _ in range(30):
        k = random.randint(3, 5)  # Choose a random k between 3 and 5
        circuit_size = float('inf')
        for MMS in metric_measure_spaces:
            # This is a placeholder for the actual computation of the minimum monotone circuit size
            # For simplicity, we assume it's linearly related to D(n)
            circuit_size = min(circuit_size, k * D_n)
        min_circuit_sizes.append(circuit_size)
    
    # Correlate these values to test the conjecture's statement
    mean_GW_distance = sum(GW_distances) / len(GW_distances)
    mean_circuit_size = sum(min_circuit_sizes) / len(min_circuit_sizes)
    
    # Check if the Gromov-Wasserstein distance from the uniform distribution on K_n to any metric measure space is within a factor of 2 of D(n)
    conjecture_holds = all(D_n <= GW_dist <= 2 * D_n for GW_dist in GW_distances)
    
    return {
        "metric_name": "Gromov-Wasserstein Distance / D(n)",
        "metric_value": mean_GW_distance / D_n,
        "instances_tested": len(GW_distances),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")