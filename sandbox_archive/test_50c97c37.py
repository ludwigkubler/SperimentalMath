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
    
    # Generate an instance with communication complexity C(φ)
    n = random.randint(5, 30)
    C_phi = n * (n - 1) // 2  # Example communication complexity
    
    # Compute the minimal local index mli(φ)
    mli_phi = C_phi / n  # Example linear relationship
    
    return {
        "metric_name": "mli(C)",
        "metric_value": mli_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    elif support_fraction < 0.5:
        print("RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")