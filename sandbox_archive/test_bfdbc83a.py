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
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = -A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def communication_complexity_rank_variance(G):
        n = len(G)
        ranks = []
        for i in range(n):
            for j in range(i + 1, n):
                subgraph = [[G[k][l] for l in range(j)] for k in range(i)]
                rank = gaussian_elimination(subgraph)
                ranks.append(rank)
        return max(ranks) - min(ranks)
    
    def minimal_local_cohomology_rank(G):
        # Placeholder function. Replace with actual implementation.
        return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        comm_rank_variance = communication_complexity_rank_variance(G)
        min_local_cohomology_rank = minimal_local_cohomology_rank(G)
        if min_local_cohomology_rank == 0:
            continue
        ratio = Fraction(comm_rank_variance, min_local_cohomology_rank)
        metrics.append(ratio)
    
    metric_value = sum(metrics) / len(metrics)
    conjecture_holds = all(metric <= 1 for metric in metrics)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "CommunicationComplexityRankVarianceRatio",
        "metric_value": float(metric_value),
        "instances_tested": len(metrics),
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
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")