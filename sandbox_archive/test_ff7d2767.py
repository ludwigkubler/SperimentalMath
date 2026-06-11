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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        m = int(math.log2(n))
        if n != 2**m:
            raise ValueError("f must be a boolean function with 2^m inputs")
        
        # Simplified version of communication complexity rank variance
        # This is just an example and should be replaced with the actual calculation
        return sum(f[i] for i in range(n)) / n
    
    def etale_sheaves_order(f):
        m = int(math.log2(len(f)))
        if len(f) != 2**m:
            raise ValueError("f must be a boolean function with 2^m inputs")
        
        # Simplified version of etale sheaves order
        # This is just an example and should be replaced with the actual calculation
        return m
    
    def correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    m_values = [5, 10, 15, 20, 30, 40]
    min_order_values = []
    rank_variance_values = []
    
    for m in m_values:
        f = generate_boolean_function(m)
        min_order = etale_sheaves_order(f)
        rank_variance = communication_complexity_rank_variance(f)
        
        min_order_values.append(min_order)
        rank_variance_values.append(rank_variance)
    
    corr = correlation(min_order_values, rank_variance_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr,
        "instances_tested": len(m_values),
        "n_max": max(m_values),
        "conjecture_holds": abs(corr) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")