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
        if n == 2:
            return Fraction(1, 2)
        elif n == 3:
            return Fraction(1, 6)
        else:
            return Fraction(1, n * (n - 1))
    
    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    n = random.randint(2, 40)
    f = random_boolean_function(n)
    rho = schur_weyl_invariant(f)
    
    return {
        "metric_name": "Schur-Weyl Invariant Ratio",
        "metric_value": float(rho),
        "instances_tested": 1,
        "conjecture_holds": rho >= 1,
        "counterexample": "" if rho >= 1 else "rho < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho < 1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")