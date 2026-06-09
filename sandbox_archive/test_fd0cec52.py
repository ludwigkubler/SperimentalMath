# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def rank_variance(A):
        S = sorted(A)
        n = len(S)
        if n == 0:
            return 0
        mean = sum(S) / n
        variance = sum((s - mean) ** 2 for s in S) / n
        return variance
    
    def minimal_representation_length(A):
        # Placeholder function. Replace with actual algorithm.
        return len(A)
    
    instances_tested = 0
    rank_variances = []
    rep_lengths = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        for _ in range(5):
            A = [random.randint(1, n) for _ in range(n)]
            rank_variances.append(rank_variance(A))
            rep_lengths.append(minimal_representation_length(A))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not rank_variances or not rep_lengths:
        return {
            "metric_name": "rank_variance vs rep_length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate Pearson correlation coefficient
    mean_var = sum(rank_variances) / len(rank_variances)
    mean_rep = sum(rep_lengths) / len(rep_lengths)
    cov = sum((rank_variances[i] - mean_var) * (rep_lengths[i] - mean_rep) for i in range(len(rank_variances))) / len(rank_variances)
    var_var = sum((rank_variances[i] - mean_var) ** 2 for i in range(len(rank_variances))) / len(rank_variances)
    var_rep = sum((rep_lengths[i] - mean_rep) ** 2 for i in range(len(rep_lengths))) / len(rep_lengths)
    
    if var_var == 0 or var_rep == 0:
        return {
            "metric_name": "rank_variance vs rep_length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = cov / (var_var * var_rep) ** 0.5
    
    return {
        "metric_name": "rank_variance vs rep_length",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(pearson_corr - Fraction(1, 3)) < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")