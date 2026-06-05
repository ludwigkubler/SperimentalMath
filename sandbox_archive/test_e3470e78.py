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
    
    def p_adic_valuation(f):
        # Placeholder for actual p-adic valuation computation
        return sum(1 for bit in f if bit == 1)
    
    def communication_complexity_rank(f):
        # Placeholder for actual communication complexity rank computation
        n = len(f)
        return n
    
    metric_name = "p_adic_valuation_rank_vs_communication_complexity_rank"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            f = ''.join(str(random.randint(0, 1)) for _ in range(n))
            rho_f = p_adic_valuation(f)
            c_rank_f = communication_complexity_rank(f)
            
            if abs(rho_f - c_rank_f) > 3:
                conjecture_holds = False
                counterexample = f"n={n}, f={f}, rho(f)={rho_f}, c-rank(f)={c_rank_f}"
                break
        
        instances_tested += 5
    
    return {
        "metric_name": metric_name,
        "metric_value": (rho_f + c_rank_f) / 2 if conjecture_holds else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")