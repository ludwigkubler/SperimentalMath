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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(circuit):
        depth = 0
        while any(x == 2 for x in circuit):
            circuit = [x if x != 2 else (circuit[i] + circuit[i+1]) % 2 for i in range(len(circuit) - 1)]
            depth += 1
        return depth
    
    def affine_quotient_group(circuit):
        n = int(math.log2(len(circuit)))
        G_C = set()
        for i in range(2**n):
            row = []
            for j in range(n):
                row.append((i >> j) & 1)
            G_C.add(tuple(row))
        return G_C
    
    def min_generators(group):
        n = len(group)
        generators = []
        for elem in group:
            if all(elem[i] == (elem[j] + elem[(j+1) % n]) % 2 for j in range(n)):
                generators.append(elem)
        return len(generators)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_max = 0
    metric_values = []
    generators_counts = []
    proof_depths = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        n_max = max(n_max, n)
        
        circuit = generate_circuit(n)
        depth = frege_proof_depth(circuit)
        G_C = affine_quotient_group(circuit)
        g = min_generators(G_C)
        
        metric_values.append(g / depth**2)
        generators_counts.append(g)
        proof_depths.append(depth)
    
    correlation = pearson_correlation(proof_depths, generators_counts)
    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = correlation >= 0.8 and max(metric_values) <= 10
    
    return {
        "metric_name": "g/d^2",
        "metric_value": mean_metric_value,
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")