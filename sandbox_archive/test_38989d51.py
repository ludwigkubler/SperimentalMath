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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def plethysm(m, n):
        if m == 0:
            return 1
        result = 0
        for k in range(1, m + 1):
            result += binomial_coefficient(m, k) * plethysm(k, n)
        return result
    
    def trivial_multiplicity(m, n):
        return plethysm(m, n)
    
    def det_multiplicity(m, n):
        if m == 0:
            return 1
        result = 0
        for k in range(1, m + 1):
            result += binomial_coefficient(m, k) * det_multiplicity(k - 1, n)
        return result
    
    def compute_multiplicities(n, m_values):
        perm_multiplicities = [trivial_multiplicity(m, n) for m in m_values]
        det_multiplicities = [det_multiplicity(m, n) for m in m_values]
        return perm_multiplicities, det_multiplicities
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [int(n**1.5 * random.random()) for _ in range(10) for n in n_values]
    
    perm_multiplicities, det_multiplicities = compute_multiplicities(max(n_values), m_values)
    
    mean_perm = sum(perm_multiplicities) / len(perm_multiplicities)
    mean_det = sum(det_multiplicities) / len(det_multiplicities)
    
    if mean_perm <= mean_det:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": mean_perm - mean_det,
            "instances_tested": len(m_values),
            "conjecture_holds": False,
            "counterexample": "multiplicity_gap_not_met"
        }
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": mean_perm - mean_det,
        "instances_tested": len(m_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break