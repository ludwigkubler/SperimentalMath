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
    
    def p_adic_log(x, p):
        if x == 0:
            return float('-inf')
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count
    
    def rank_variance(protocols):
        n = len(protocols)
        mean_rank = sum(protocol['rank'] for protocol in protocols) / n
        variance = sum((protocol['rank'] - mean_rank) ** 2 for protocol in protocols) / n
        return variance
    
    def p_adic_growth_variability(protocols, p):
        growths = [p_adic_log(C(P), p) for P in protocols]
        mean_growth = sum(growths) / len(growths)
        variability = sum((g - mean_growth) ** 2 for g in growths) / len(growths)
        return variability
    
    def C(protocol):
        # Placeholder complexity function
        return protocol['complexity']
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        protocols = [{'rank': random.randint(1, 10), 'complexity': random.randint(1, 100)} for _ in range(n)]
        rank_var = rank_variance(protocols)
        p_adic_var = p_adic_growth_variability(protocols, 2)  # Using base 2 for simplicity
        results.append({'n': n, 'rank_var': rank_var, 'p_adic_var': p_adic_var})
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No protocols generated"
        }
    
    mean_rank_var = sum(result['rank_var'] for result in results) / len(results)
    mean_p_adic_var = sum(result['p_adic_var'] for result in results) / len(results)
    correlation_coefficient = sum((result['rank_var'] - mean_rank_var) * (result['p_adic_var'] - mean_p_adic_var) 
                                  for result in results) / len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and correlation_coefficient <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed {first_failing_seed}\"")
    else:
        mean_metric_value = sum(result['metric_value'] for result in results) / len(results)
        support_fraction = sum(1 for result in results if abs(result['metric_value']) > 0.8 and result['metric_value'] <= 3) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")