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

def generate_kcnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([0, 1]) - 1) for _ in range(random.randint(1, n))]
        if len(set(clause)) == len(clause):  # Ensure no duplicate literals
            clauses.append(clause)
    return clauses

def compute_padic_order(n):
    return round(n ** (1/3))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        m = int(0.5 * n)  # Clause density between 0.5 and 1
        phi = generate_kcnf(n, m)
        
        padic_order = compute_padic_order(n)
        total_metric_value += padic_order
        instances_tested += 1
        
        if n > n_max:
            n_max = n
    
    metric_name = 'padic_order'
    metric_value = total_metric_value / instances_tested
    conjecture_holds = all(padic_order <= n ** (1/3) for padic_order in [compute_padic_order(n) for n in [5, 10, 15, 20, 30, 40]])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'n_max': n_max,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r['conjecture_holds']) / len(all_results)
    
    if all(r['conjecture_holds'] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")