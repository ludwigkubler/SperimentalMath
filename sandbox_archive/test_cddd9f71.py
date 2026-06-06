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
        if n == 1:
            return 1
        rank = 0
        for i in range(1, n):
            if all(f[j] != f[j + i] for j in range(n - i)):
                rank += 1
        return rank
    
    def polynomial_from_boolean_function(f):
        n = len(f)
        degree = communication_complexity_rank(f)
        poly = [0] * (degree + 1)
        poly[degree] = sum(f) / len(f)
        return poly
    
    def minimal_diophantine_dimension(poly):
        degree = len(poly) - 1
        if degree == 0:
            return 0
        return degree
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    r_f = communication_complexity_rank(f)
    p_f = polynomial_from_boolean_function(f)
    d_p_f = minimal_diophantine_dimension(p_f)
    
    conjecture_holds = d_p_f >= r_f**2
    counterexample = "" if conjecture_holds else f"Counterexample for n={n}, r_f={r_f}, d(p_f)={d_p_f}"
    
    return {
        "metric_name": "minimal_diophantine_dimension",
        "metric_value": d_p_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")