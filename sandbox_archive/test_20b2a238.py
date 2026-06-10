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
    
    def generate_protocol(n):
        protocol = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return protocol
    
    def lie_algebroid_cohomology_rank(protocol):
        n = len(protocol)
        A = [[sum(row[i] * col[j] for row in protocol) for j in range(n)] for i in range(n)]
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i, n)):
                continue
            rank += 1
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        
        return rank
    
    def rank_variance(protocol):
        n = len(protocol)
        total = sum(sum(row) for row in protocol)
        variance = sum((sum(row) - total / n) ** 2 for row in protocol) / n
        return variance
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        protocol = generate_protocol(n)
        cohomology_rank = lie_algebroid_cohomology_rank(protocol)
        rank_variance_value = rank_variance(protocol)
        
        results.append({
            "n": n,
            "cohomology_rank": cohomology_rank,
            "rank_variance": rank_variance_value
        })
    
    if not results:
        return {
            "metric_name": "cohomology_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cohomology_ranks = [result["cohomology_rank"] for result in results]
    rank_variances = [result["rank_variance"] for result in results]
    
    mean_cohomology_rank = sum(cohomology_ranks) / len(cohomology_ranks)
    std_cohomology_rank = math.sqrt(sum((x - mean_cohomology_rank) ** 2 for x in cohomology_ranks) / len(cohomology_ranks))
    
    conjecture_holds = all(x >= y ** 0.5 for x, y in zip(cohomology_ranks, rank_variances))
    counterexample = "" if conjecture_holds else "cohomology_rank < sqrt(rank_variance)"
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": mean_cohomology_rank,
        "instances_tested": len(cohomology_ranks),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")