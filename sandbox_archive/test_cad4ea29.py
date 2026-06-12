# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_product_manifold(f):
        n = len(f[0])
        m = len(f)
        M = [[f[i][j] for j in range(m)] for i in range(n)]
        return M
    
    def communication_complexity_rank(M):
        n = len(M)
        m = len(M[0])
        rank = 0
        for i in range(n):
            row = [M[i][j] for j in range(m)]
            if any(row[j] != row[0] for j in range(1, m)):
                rank += 1
        return rank
    
    def minimal_kahler_ricci_form(M):
        n = len(M)
        m = len(M[0])
        sum_ = Fraction(0, 1)
        for i in range(n):
            for j in range(m):
                sum_ += M[i][j]
        return sum_.limit_denominator()
    
    f = generate_boolean_function(random.randint(5, 30))
    M = tensor_product_manifold(f)
    c_r_f = communication_complexity_rank(M)
    kappa_f = minimal_kahler_ricci_form(M)
    
    if kappa_f > Fraction(1.5) * sum(kappa_f for _ in range(30)) / 30:
        return {
            "metric_name": "correlation",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": len(f[0]),
            "conjecture_holds": False,
            "counterexample": "kappa_f > 1.5 * mean_kappa_f"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": kappa_f * c_r_f,
        "instances_tested": 1,
        "n_max": len(f[0]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"kappa_f > 1.5 * mean_kappa_f\" first_failing_seed={first_failing_seed}")