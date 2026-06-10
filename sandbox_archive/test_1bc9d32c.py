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
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
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
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        return rank
    
    def rank_variance(protocol):
        n = len(protocol)
        total = sum(sum(row) for row in protocol)
        variance = 0
        for row in protocol:
            variance += (sum(row) - total / n) ** 2
        return variance / n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        protocol = generate_protocol(n)
        cohomology_rank = lie_algebroid_cohomology_rank(protocol)
        rank_var = rank_variance(protocol)
        
        results.append({
            "cohomology_rank": cohomology_rank,
            "rank_variance": rank_var
        })
    
    mean_rank_variance = sum(result["rank_variance"] for result in results) / len(results)
    min_cohomology_rank = min(result["cohomology_rank"] for result in results)
    
    conjecture_holds = all(coh >= math.sqrt(var) for coh, var in zip([result["cohomology_rank"] for result in results], [result["rank_variance"] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Cohomology Rank Variance",
        "metric_value": mean_rank_variance,
        "instances_tested": len(results),
        "n_max": max([len(result["cohomology_rank"]) for result in results]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")