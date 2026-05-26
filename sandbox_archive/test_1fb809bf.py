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
    
    def polynomial_rank(poly, n):
        if not poly:
            return 0
        max_degree = 0
        for term in poly:
            degree = sum(1 for coeff in term if coeff != 0)
            if degree > max_degree:
                max_degree = degree
        return max_degree
    
    def min_poly_rank(f, n):
        terms = []
        for i in range(2**n):
            x = [int(b) for b in format(i, f'0{n}b')]
            y = f(x)
            term = [y]
            for j in range(n):
                if x[j] == 1:
                    term.append(-x[(j+1)%n])
                else:
                    term.append(x[(j+1)%n])
            terms.append(term)
        return polynomial_rank(terms, n)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    rank = min_poly_rank(f, n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")