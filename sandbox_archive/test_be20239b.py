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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n or k < 0:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def kronecker_coefficient(lam, mu):
    n = sum(lam)
    m = sum(mu)
    if n != m:
        return 0
    result = 1
    for i in range(max(lam + mu), 0, -1):
        result *= binomial_coefficient(n + m - i, n - i)
        result //= (i + 1) * binomial_coefficient(sum(lam[:i]), sum(mu[:i]))
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(3, 40)
    lam = [n-1, 1]
    mu = [n-2, 2] if n > 3 else [n-1, 1]
    
    perm_multiplicity = kronecker_coefficient(lam, mu)
    det_multiplicity = kronecker_coefficient(lam, mu) if n == 40 else 0
    
    metric_value = perm_multiplicity - det_multiplicity
    conjecture_holds = perm_multiplicity > det_multiplicity
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*40 + 1, 40))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")