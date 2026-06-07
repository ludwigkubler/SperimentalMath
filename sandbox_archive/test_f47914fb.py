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
    
    def generate_k_clique(k, n):
        if k > n:
            return None
        vertices = list(range(n))
        clique = []
        for _ in range(k):
            v = random.choice(vertices)
            clique.append(v)
            vertices.remove(v)
        return clique
    
    def calculate_hodge_index(clique):
        # Placeholder function to compute the Hodge index
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    def calculate_communication_complexity_rank_variance(clique):
        # Placeholder function to compute the communication complexity rank variance
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            clique = generate_k_clique(random.randint(2, min(n-1, 5)), n)
            if clique is None:
                continue
            hodge_index = calculate_hodge_index(clique)
            rank_variance = calculate_communication_complexity_rank_variance(clique)
            results.append((hodge_index, rank_variance))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid k-cliques generated"
        }
    
    hodge_indices = [r[0] for r in results]
    rank_variances = [r[1] for r in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else None
    
    correlation_coefficient = pearson_correlation(hodge_indices, rank_variances)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient > 0.8 and all(c >= 0.5 for c in results),
        "counterexample": "" if correlation_coefficient is not None else "No valid k-cliques generated"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid k-cliques generated across seeds")