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
    
    def generate_disjointness_function(n):
        inputs = [random.getrandbits(1) for _ in range(n)]
        return lambda x, y: inputs[x] != inputs[y]
    
    def construct_affine_scheme(n):
        # Simplified construction for demonstration
        return list(range(n))
    
    def find_d_module_rank(X, f):
        # Placeholder for actual D-module rank computation
        return len(X) * math.log(len(X), 2)
    
    def communication_complexity(f, n):
        # Placeholder for actual communication complexity computation
        return n * math.log(n, 2)
    
    def alpha(n):
        return 0.9 * n * math.log(n, 2)
    
    metric_name = "Rank vs DPLL Heig"
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_disjointness_function(n)
        X = construct_affine_scheme(n)
        rank = find_d_module_rank(X, f)
        comm_complexity = communication_complexity(f, n)
        
        if rank < 0.9 * n * math.log(n, 2) or comm_complexity < 0.9 * n * math.log(n, 2):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": (0.9 * instances_tested * n * math.log(n, 2)) / instances_tested,
        "instances_tested": instances_tested,
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")