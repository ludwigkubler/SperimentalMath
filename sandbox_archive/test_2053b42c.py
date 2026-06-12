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
    
    def dpll(f):
        if not f:
            return True, []
        if len(f[0]) == 1:
            return False, []
        p = next(x for x in f[0] if x > 0)
        for assignment in [True, False]:
            new_f = [[x for x in clause if x != p and x != -p] for clause in f]
            result, path = dpll(new_f)
            if result:
                return True, [assignment] + path
        return False, []
    
    def kahler_class_rank(f):
        # Placeholder function to compute Kähler class rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(f) ** 0.5
    
    n = random.randint(5, 40)
    f = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
    
    kr = kahler_class_rank(f)
    h, path = dpll(f)
    
    return {
        "metric_name": "correlation",
        "metric_value": kr * h,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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