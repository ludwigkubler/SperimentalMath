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
    
    def gamma(n):
        if n == 1 or n == 0:
            return 1
        else:
            return (n - 1) * gamma(n - 1)
    
    def hypergeometric_moment(n, k):
        return math.comb(n, k) / gamma(2 + n / 2)
    
    def resolution_proof_length(n):
        # Placeholder function for actual proof length calculation
        return random.randint(1, 100 * n**3)
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i for i in range(len(x))}
        y_ranks = {y[i]: i for i in range(len(y))}
        n = len(x)
        numerator = sum((x_ranks[x[i]] - y_ranks[y[i]])**2 for i in range(n))
        denominator = 6 * (sum((x[i] - y[i])**2 for i in range(n)) / n)
        return 1 - numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        moments = [hypergeometric_moment(n, k) for k in range(n + 1)]
        proof_lengths = [resolution_proof_length(n) for _ in range(30)]
        log_moments = [math.log(m) for m in moments]
        
        if len(log_moments) != len(proof_lengths):
            return {
                "metric_name": "Spearman Rank Correlation",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mismatched_lengths"
            }
        
        correlation = spearman_rank_correlation(log_moments, proof_lengths)
        results.append(correlation)
    
    avg_corr = sum(results) / len(results)
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": avg_corr,
        "instances_tested": 180,
        "conjecture_holds": avg_corr > 0.99,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    avg_metric = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r > 0.99) / len(results)
    
    if all(r > 0.99 for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={math.sqrt(sum((r - avg_metric)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric} std={math.sqrt(sum((r - avg_metric)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r <= 0.99)]
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")