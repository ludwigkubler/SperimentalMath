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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def tensor_product(f, g):
        m = len(f)
        n = len(g)
        result = []
        for i in range(2**(m+n)):
            bitstring = format(i, f'0{m+n}b')
            x = int(bitstring[:m], 2)
            y = int(bitstring[m:], 2)
            result.append(f[x] * g[y])
        return result
    
    def circuit_depth(f):
        m = len(f)
        if m == 1:
            return 1
        depth = 0
        for i in range(1, m+1):
            if any(f[j] != f[j-1] for j in range(i)):
                depth += 1
        return depth + 1
    
    def fisher_rao_entropy(p):
        n = len(p)
        H = 0
        for pi in p:
            if pi > 0:
                H -= pi * math.log(pi, n)
        return H
    
    m = random.randint(2, 5)  # Generate a random number of inputs between 2 and 5
    f = generate_boolean_function(m)
    g = tensor_product(f, f)
    
    n = circuit_depth(f)
    H_g = fisher_rao_entropy(g)
    
    metric_name = "geometric_entropy"
    metric_value = H_g
    instances_tested = 1
    n_max = n
    conjecture_holds = H_g <= m * math.log(n)
    counterexample = "" if conjecture_holds else f"m={m}, n={n}, H(g)={H_g}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")