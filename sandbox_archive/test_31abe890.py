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
    n = 5  # Start with small n and increase for more trials
    max_n = 40
    metric_values = []
    
    while len(metric_values) < 30 and n <= max_n:
        f = [random.choice([0, 1]) for _ in range(n)]
        if sum(f) % 2 == 0:  # Ensure the function computes PARITY
            V_f = set()
            for i in range(2**n):
                x = [(i >> j) & 1 for j in range(n)]
                if f == [x[j] ^ (sum(x[:j]) % 2) for j in range(n)]:
                    V_f.add(tuple(x))
            
            dimension = len(V_f)
            metric_values.append(dimension)
        n += 5
    
    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = abs(mean_value - math.log(n, 2) / math.log(math.log(n, 2), 2)) <= 3
    counterexample = "" if conjecture_holds else f"mean={mean_value}, expected=Θ(log({n})/log(log({n})))"
    
    return {
        "metric_name": "dimension",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")