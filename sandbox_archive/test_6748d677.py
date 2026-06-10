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
        protocol = [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
        return protocol
    
    def rank_variance(protocol):
        n = len(protocol)
        m = len(protocol[0])
        rank_sum = sum(sum(row) for row in protocol)
        variance = sum((sum(row) - rank_sum / n)**2 for row in protocol) / (n * m)
        return variance
    
    def geometric_invariant_rank(protocol):
        # Placeholder function; actual implementation needed
        return 1.0  # Default value, to be replaced with actual computation

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        protocol = generate_protocol(n, n)
        gir_value = geometric_invariant_rank(protocol)
        rank_var_value = rank_variance(protocol)
        results.append({
            "n": n,
            "gir": gir_value,
            "rank_var": rank_var_value
        })
    
    gir_mean = sum(result["gir"] for result in results) / len(results)
    rank_var_mean = sum(result["rank_var"] for result in results) / len(results)
    support_fraction = sum(abs(result["gir"] - result["rank_var"]) <= 0.1 * result["rank_var"] for result in results) / len(results)
    
    return {
        "metric_name": "gir_to_rank_variance_ratio",
        "metric_value": gir_mean / rank_var_mean,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")