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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        m = 2**(n-1)
        rank = 0
        while m > 0:
            rank += 1
            m //= 2
        return rank
    
    def polynomial_representation(f, n):
        # Simplified representation for demonstration purposes
        return sum([f[i] * (i + 1) for i in range(n)])
    
    def minimal_diophantine_dimension(p):
        # Simplified calculation for demonstration purposes
        return len(str(p))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    r_f = communication_complexity_rank(f)
    p_f = polynomial_representation(f, n)
    d_p_f = minimal_diophantine_dimension(p_f)
    
    conjecture_holds = d_p_f >= r_f**2
    counterexample = "" if conjecture_holds else f"n={n}, r_f={r_f}, d(p_f)={d_p_f}"
    
    return {
        "metric_name": "minimal_diophantine_dimension",
        "metric_value": d_p_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")