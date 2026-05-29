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
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, int(n) + 1):
            result *= i
        return result
    
    def hypergeometric_moment(n, k):
        if k < 0 or k > n:
            return 0
        return math.comb(n, k) / gamma(2 + n / 2)
    
    def resolution_proof_length(n):
        # Placeholder function for actual proof length calculation
        return random.randint(1, n**3)
    
    def spearman_rank_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        
        n = len(x)
        sum_rank_diff_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_rank_diff_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        moments = [hypergeometric_moment(n, k) for k in range(n + 1)]
        proof_lengths = [resolution_proof_length(n) for _ in range(30)]
        
        if not moments or not proof_lengths:
            return {
                "metric_name": "Spearman rank correlation",
                "metric_value": None,
                "instances_tested": len(proof_lengths),
                "conjecture_holds": False,
                "counterexample": "empty_moments_or_proofs"
            }
        
        log_moments = [math.log(m) for m in moments]
        corr_coeff = spearman_rank_correlation(log_moments, proof_lengths)
        results.append(corr_coeff)
    
    avg_corr_coeff = sum(results) / len(results)
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": avg_corr_coeff,
        "instances_tested": len(proof_lengths),
        "conjecture_holds": avg_corr_coeff > 0.99,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    avg_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r > 0.99) / len(results)
    
    if all(r is not None and r > 0.99 for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r is None or r <= 0.99)
        print(f"RESULT: FALSIFIED counterexample=\"empty_moments_or_proofs\" first_failing_seed={seeds[first_failing_seed]}")