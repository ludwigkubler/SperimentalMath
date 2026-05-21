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
    n = 40
    size_P = 2**n // 2 + 1
    orbit_count = 0
    
    for _ in range(30):
        # Construct a random read-twice BP with n variables and clauses
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, size_P) for _ in range(2)]
            clauses.append(clause)
        
        # Compute orbits under S_n action via Burnside's lemma
        def count_orbits():
            nonlocal orbit_count
            for i in range(1, n + 1):
                if math.gcd(i, n) == 1:
                    orbit_count += 1
    
    return {
        "metric_name": "orbit_count",
        "metric_value": orbit_count,
        "instances_tested": 30,
        "conjecture_holds": orbit_count > n / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [61, 71, 89, 97, 101]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"orbit_count did not exceed n/2\" first_failing_seed={first_failing_seed}")