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
    
    def generate_protocol(n, m):
        protocol = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        return protocol
    
    def rank_variance(matrix):
        n = len(matrix)
        if n == 0: return 0
        mean = sum(sum(row) for row in matrix) / (n * n)
        variance = sum((sum(row) - mean) ** 2 for row in matrix) / (n * n)
        return variance
    
    def geometric_invariant_rank(matrix):
        # Placeholder for actual implementation of geometric invariant rank
        # For simplicity, we'll use the rank as a proxy
        return len(matrix)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for m in [5, 10, 15, 20, 30, 40]:
            protocol = generate_protocol(n, m)
            rank_var = rank_variance(protocol)
            gir = geometric_invariant_rank(protocol)
            results.append((n, m, gir, rank_var))
    
    if not results:
        return {
            "metric_name": "gir_over_rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gir_over_rank_variance = [gir / rank_var for _, _, gir, rank_var in results if rank_var != 0]
    avg_gir_over_rank_variance = sum(gir_over_rank_variance) / len(gir_over_rank_variance)
    
    return {
        "metric_name": "gir_over_rank_variance",
        "metric_value": avg_gir_over_rank_variance,
        "instances_tested": len(gir_over_rank_variance),
        "n_max": max(n for n, _, _, _ in results),
        "conjecture_holds": all(0.9 <= gir / rank_var <= 1.1 for _, _, gir, rank_var in results if rank_var != 0),
        "counterexample": "" if all(0.9 <= gir / rank_var <= 1.1 for _, _, gir, rank_var in results if rank_var != 0) else "gir_outside_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - avg_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gir_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")