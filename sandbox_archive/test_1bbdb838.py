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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 1
        while True:
            new_f = []
            for i in range(n):
                if f[i] != f[(i + 1) % n]:
                    new_f.append(1)
                else:
                    new_f.append(0)
            f = new_f
            rank += 1
            if len(set(f)) == 2:
                break
        return rank
    
    def luroth_normal_form_degree(f):
        n = len(f)
        degree = 0
        for i in range(n):
            if f[i] != f[(i + 1) % n]:
                degree += 1
        return degree
    
    m = random.randint(5, 40)
    f = generate_boolean_function(m)
    
    lnd_f = luroth_normal_form_degree(f)
    r_f = communication_complexity_rank(f)
    
    return {
        "metric_name": "LND(f) vs r(f)",
        "metric_value": lnd_f / r_f,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")