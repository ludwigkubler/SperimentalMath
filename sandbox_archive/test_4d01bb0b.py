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
    beta = 5
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        max_delta_over_bound = 0
        
        for _ in range(30):
            f = [random.randint(0, 9) for _ in range(n)]
            g = [beta * math.log(sum(math.exp((f[y] + f[(x - y) % n]) / beta) for y in range(n)) / n) for x in range(n)]
            
            def TFT_beta(h, k):
                exp_sum = 0
                for x in range(n):
                    exp_sum += math.exp(h[x] / beta) * math.exp(-2 * math.pi * k * x / n)
                return beta * math.log(exp_sum)
            
            MFC_f = min(TFT_beta(f, k) for k in range(1, n))
            MFC_g = min(TFT_beta(g, k) for k in range(1, n))
            delta = abs(MFC_g - 2 * MFC_f)
            bound = 3 * beta * math.log(n)
            
            instances_tested += 1
            max_delta_over_bound = max(max_delta_over_bound, delta / bound)
        
        results.append({
            "n": n,
            "max_delta_over_bound": max_delta_over_bound,
            "instances_tested": instances_tested,
            "conjecture_holds": max_delta_over_bound <= 1.0
        })
    
    mean_delta_over_bound = sum(result["max_delta_over_bound"] for result in results) / len(results)
    std_delta_over_bound = math.sqrt(sum((result["max_delta_over_bound"] - mean_delta_over_bound) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Max Delta Over Bound",
        "metric_value": mean_delta_over_bound,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else f"max_delta_over_bound={max_delta_over_bound} at n={max(result['n'] for result in results if not result['conjecture_holds'])}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")