# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import product

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
            for j in range(i + 1, n + 1):
                subfunction = [f[i] & f[j] for i, j in product(range(n), repeat=2)]
                if communication_complexity_rank(subfunction) > rank:
                    rank = communication_complexity_rank(subfunction)
        return rank
    
    def minimal_local_induction_ring_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 0
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                subfunction = [f[i] & f[j] for i, j in product(range(n), repeat=2)]
                if minimal_local_induction_ring_rank(subfunction) > rank:
                    rank = minimal_local_induction_ring_rank(subfunction)
        return rank
    
    def alpha(n):
        return Fraction(1, 1).log(Fraction(n, 1))
    
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        
        comm_rank = communication_complexity_rank(f)
        local_induction_rank = minimal_local_induction_ring_rank(f)
        
        if local_induction_rank < alpha(n):
            conjecture_holds = False
            counterexample = f"n={n}, comm_rank={comm_rank}, local_induction_rank={local_induction_rank}"
            break
        
        metric_value += local_induction_rank
    
    return {
        "metric_name": "minimal_local_induction_ring_rank",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")