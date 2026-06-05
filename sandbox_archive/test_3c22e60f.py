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
    
    def generate_geometric_vector_field(d):
        # Generate a random d-dimensional geometric vector field
        return [random.uniform(-1, 1) for _ in range(d)]
    
    def compute_holonomy_representation(vf):
        # Compute the holonomy representation (simplified example)
        n = len(vf)
        H = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fraction(1, 1)
        return H
    
    def compute_communication_complexity_rank(H):
        # Compute the communication complexity rank (simplified example)
        n = len(H)
        rank = 0
        for row in H:
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def pearsonr(x, y):
        # Compute Pearson correlation coefficient
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        return cov_xy / math.sqrt(var_x * var_y)
    
    def bootstrap_correlation(x, y, n_samples):
        # Bootstrap method to estimate correlation significance
        correlations = []
        for _ in range(n_samples):
            indices = random.sample(range(len(x)), len(x))
            sample_x = [x[i] for i in indices]
            sample_y = [y[i] for i in indices]
            correlations.append(pearsonr(sample_x, sample_y))
        return correlations
    
    d = 10
    n_samples = 100
    correlation_threshold = 0.7
    
    min_rank_holonomy = []
    comm_complexity_rank = []
    
    for _ in range(n_samples):
        vf = generate_geometric_vector_field(d)
        H = compute_holonomy_representation(vf)
        rank_comm = compute_communication_complexity_rank(H)
        
        if rank_comm < 1 or rank_comm > d:
            return {
                "metric_name": "communication_complexity_rank",
                "metric_value": None,
                "instances_tested": n_samples,
                "n_max": d,
                "conjecture_holds": False,
                "counterexample": "out_of_range"
            }
        
        min_rank_holonomy.append(min([abs(x) for row in H for x in row if x != 0]))
        comm_complexity_rank.append(rank_comm)
    
    corr = pearsonr(min_rank_holonomy, comm_complexity_rank)
    bootstrap_correlations = bootstrap_correlation(min_rank_holonomy, comm_complexity_rank, n_samples * 10)
    bootstrap_threshold = sorted(bootstrap_correlations)[int(n_samples * 10 * 0.95)]
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": corr,
        "instances_tested": n_samples,
        "n_max": d,
        "conjecture_holds": corr > correlation_threshold and all(1 <= rank <= d for rank in comm_complexity_rank),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={first_failing_seed}")