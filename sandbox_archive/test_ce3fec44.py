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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def communication_complexity_rank_variance(G):
        n = len(G)
        ranks = []
        for i in range(n):
            for j in range(i + 1, n):
                subgraph = [[G[u][v] for v in range(j)] for u in range(i)]
                rank = gaussian_elimination(subgraph)
                if rank is not None:
                    ranks.append(rank)
        if not ranks:
            return 0
        max_rank = max(ranks)
        min_rank = min(ranks)
        variance = (max_rank - min_rank) ** 2 / len(ranks)
        return variance
    
    def minimal_local_cohomology_rank(G):
        n = len(G)
        rank = sum(1 for row in G if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        comm_rank_variance = communication_complexity_rank_variance(G)
        min_local_cohomology_rank = minimal_local_cohomology_rank(G)
        if min_local_cohomology_rank == 0:
            continue
        ratio = Fraction(comm_rank_variance, min_local_cohomology_rank)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(r <= mean_ratio for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Communication Complexity Rank Variance to Minimal Local Cohomology Rank",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= mean_ratio) / len(results)
    if support_fraction >= 0.8:
        result = f"SUPPORTED mean={mean_ratio} std={math.sqrt(sum((r - mean_ratio) ** 2 for r in results) / len(results))} support_fraction={support_fraction}"
    elif any(r > mean_ratio for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        result = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE mapping_undefined"
    
    print(result)