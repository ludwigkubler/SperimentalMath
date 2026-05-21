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
    
    def monotone_dnf_formula(truth_table):
        n = len(truth_table)
        dnf = []
        for i in range(n):
            if truth_table[i][i] == 1:
                clause = [j for j in range(n) if truth_table[j][i] == 1]
                dnf.append(clause)
        return dnf
    
    def polynomial_hierarchy_depth(dnf, n, k):
        # Simplified algorithm to compute the depth
        depth = 0
        while True:
            new_dnf = []
            for clause in dnf:
                if all(len(c) > 1 for c in clause):
                    new_clause = [tuple(sorted(c)) for c in clause]
                    new_dnf.append(new_clause)
            if len(new_dnf) == 0:
                break
            dnf = new_dnf
            depth += 1
        return depth
    
    def k_clique_instance(n, k):
        # Generate a random k-clique instance
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    n_max = 40
    k_max = 5
    results = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            vertices, edges = k_clique_instance(n, random.randint(2, min(k_max, n - 1)))
            truth_table = [[0] * n for _ in range(n)]
            for u, v in edges:
                truth_table[u][v] = truth_table[v][u] = 1
            dnf = monotone_dnf_formula(truth_table)
            depth = polynomial_hierarchy_depth(dnf, n, k_max)
            results.append({
                "metric_name": "polynomial_hierarchy_depth",
                "metric_value": depth,
                "instances_tested": 1,
                "conjecture_holds": depth <= (n ** k_max) / 2,
                "counterexample": "" if depth <= (n ** k_max) / 2 else f"Depth {depth} exceeds n^{k_max}/2"
            })
    
    mean_depth = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_depth": mean_depth,
        "std_dev": std_dev,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    print("TRIALS:")
    for result in results:
        print(f"TRIAL: {result}")
    
    mean_depth = sum(result["mean_depth"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["mean_depth"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")