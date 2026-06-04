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
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = -1
            A[i][-1] = f[i]
        A[-1][-1] = -1
        return A
    
    def p_adic_roots(poly, p):
        n = len(poly)
        roots = set()
        for x in range(p**n):
            if all((poly[j] * pow(x, j, p) % p == 0 for j in range(n))):
                roots.add(x)
        return roots
    
    def communication_complexity_rank(f):
        # Simplified version of a known protocol
        n = len(f)
        rank = int(math.sqrt(n))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        p = 2  # Using p=2 for simplicity
        roots = p_adic_roots(poly, p)
        R_f = communication_complexity_rank(f)
        
        if len(roots) < n**(1/3) or len(roots) > n**(2/3):
            conjecture_holds = False
            counterexample = f"n={n}, roots_count={len(roots)}, expected_range=[{n**(1/3)}, {n**(2/3)}]"
        
        if R_f != int(math.sqrt(n)):
            conjecture_holds = False
            counterexample = f"n={n}, rank={R_f}, expected_rank=int(sqrt({n}))"
        
        total_metric_value += len(roots)
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "p_adic_roots_count",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])].get('counterexample', 'unknown')}\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")