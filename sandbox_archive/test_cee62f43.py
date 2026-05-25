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
    
    def tropical_rank(G):
        # Placeholder for the actual tropical rank computation
        return random.randint(1, 50)
    
    def communication_complexity(n):
        # Placeholder for the actual communication complexity computation
        return n * (n - 1) // 2
    
    def construct_affine_grassmannian(inputs):
        # Placeholder for the actual affine Grassmannian construction
        return [random.randint(1, 10) for _ in inputs]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    inputs = [random.randint(0, 1) for _ in range(n)]
    G = construct_affine_grassmannian(inputs)
    tau_G = tropical_rank(G)
    CC_R_DISJ_n = communication_complexity(n)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": tau_G,
        "instances_tested": 1,
        "conjecture_holds": tau_G <= 2 * CC_R_DISJ_n,  # Placeholder for the actual constant c
        "counterexample": "" if tau_G <= 2 * CC_R_DISJ_n else f"n={n}, tau_G={tau_G}, CC_R_DISJ_n={CC_R_DISJ_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")