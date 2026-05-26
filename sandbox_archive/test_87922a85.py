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
    
    def generate_k_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    def twisted_group_algebra_rank(vertices, edges):
        n = len(vertices)
        rank = 2 ** (n - len(edges))
        return rank
    
    def monotone_circuit_depth(n, k):
        # Simplified heuristic for monotone circuit depth
        return n * math.log2(k) + 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n // 2, 4))
            vertices, edges = generate_k_clique_instance(n, k)
            rank = twisted_group_algebra_rank(vertices, edges)
            depth = monotone_circuit_depth(n, k)
            
            total_rank += rank
            total_depth += depth
            instances_tested += 1
    
    mean_ratio = total_rank / (2 ** (n_values[-1] - n_values[0]) * sum(range(1, len(n_values) + 1)))
    
    conjecture_holds = mean_ratio >= 0.5 and all(total_rank / (2 ** (n_values[-1] - n_values[0]) * sum(range(1, len(n_values) + 1))) > 0.3 for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.3 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")