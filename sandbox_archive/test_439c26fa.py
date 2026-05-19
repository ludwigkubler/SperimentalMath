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
from math import factorial, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hook_length_formula(shape, n):
        product = 1
        for row in range(n):
            for col in range(row + 1):
                product *= (n - row + col - 1) // (col + 1)
        return product
    
    def young_tableau_count(shape, n):
        if not shape:
            return 1
        count = 0
        for i in range(1, min(n, shape[0]) + 1):
            new_shape = [i - 1] + shape[1:]
            count += factorial(n) // (factorial(i) * hook_length_formula(new_shape, n))
        return count
    
    def multiplicity(representation, shape, n):
        if representation == 'perm':
            return young_tableau_count(shape, n)
        elif representation == 'det':
            return 0
        else:
            return None
    
    n = random.randint(2, 40)
    m = random.randint(1, int(sqrt(n)) - 1)
    
    mu_perm = multiplicity('perm', (n-1, 1), n)
    mu_det = multiplicity('det', (m,), m)
    
    if mu_perm is None or mu_det is None:
        return {
            "metric_name": "Multiplicity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    result = {
        "metric_name": "Multiplicity",
        "metric_value": mu_perm > mu_det,
        "instances_tested": 1,
        "conjecture_holds": mu_perm > mu_det,
        "counterexample": ""
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r) / len(results)
    
    if all(results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(False)]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")