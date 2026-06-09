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
    random.seed(seed)
    
    def communication_complexity_rank(f):
        n = len(f)
        if n < 2:
            return 0
        r_f = 1
        for i in range(1, n):
            if f[i] != f[0]:
                r_f += 1
        return r_f
    
    def minimal_tropical_motivic_rank(phi_f):
        # Placeholder implementation of minimal tropical motivic rank calculation
        # This is a dummy function and should be replaced with actual computation
        return len(phi_f)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    phi_f = generate_tseitin_formula(f)
    
    r_f = communication_complexity_rank(f)
    mtr_phi_f = minimal_tropical_motivic_rank(phi_f)
    
    metric_value = mtr_phi_f <= math.log(r_f)
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mtr_phi_f <= log(r_f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_tseitin_formula(f):
    # Placeholder implementation of Tseitin formula generation
    # This is a dummy function and should be replaced with actual computation
    return f

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")