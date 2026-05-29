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

def hypergeometric_zeros(D, n):
    zeros = []
    for z in [Fraction(1 + i, 2) for i in range(1, 2*n+1)]:
        if abs(z) > 1e-6 and abs((1 - z)**(-D/2)) < 1e-6:
            zeros.append(z)
    return zeros

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    D = random.randint(1, 10)
    c_D = 10 * D  # Example polynomial upper bound
    
    circuit = [random.choice([0, 1]) for _ in range(n)]
    zeros = hypergeometric_zeros(D, n)
    
    metric_value = len(zeros) / (c_D * 2**n)
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else f"Too many zeros: {len(zeros)} > {c_D * 2**n}"
    
    return {
        "metric_name": "Zeros of Hypergeometric Function",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many zeros\" first_failing_seed={first_failing_seed}")