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
    
    def schur_weyl_invariant(f):
        n = len(f)
        rho_s = 0
        rho_t = 0
        for i in range(2**n):
            bitstring = format(i, f'0{n}b')
            value = int(bitstring, 2)
            if value == f(value):
                rho_s += 1
            rho_t += 1
        return Fraction(rho_s, rho_t)

    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    n = random.randint(5, 40)
    f = random_boolean_function(n)
    rho_f = schur_weyl_invariant(f)
    
    if rho_f < Fraction(1, 2):
        return {
            "metric_name": "Schur-Weyl Invariant Ratio",
            "metric_value": float(rho_f),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho(f) = {rho_f} < c(n)"
        }
    
    return {
        "metric_name": "Schur-Weyl Invariant Ratio",
        "metric_value": float(rho_f),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 6)]  # Using a small set of primes as default
    else:
        seeds = list(map(int, sys.argv[1:]))

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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho(f) < c(n)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")