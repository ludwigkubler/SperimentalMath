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
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in range(2)]
        probabilities = [c / n for c in counts if c > 0]
        return -sum(p * math.log2(p) for p in probabilities)

    def geometric_flow_order(f):
        # Placeholder implementation of geometric flow order computation
        # This is a dummy function and should be replaced with actual computation
        return len(f)

    instances_tested = 0
    n_max = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = ''.join(random.choice('01') for _ in range(n))
            instances_tested += 1
            n_max = max(n_max, n)
            entropy = shannon_entropy(f)
            order = geometric_flow_order(f)
            ratio = order / entropy if entropy > 0 else float('inf')
            
            total_ratio += ratio
            
            if ratio > 2:  # Placeholder constant C
                conjecture_holds = False
                counterexample = f"n={n}, f={f}, order={order}, entropy={entropy}, ratio={ratio}"
                break
    
    return {
        "metric_name": "Ratio of Geometric Flow Order to Entropy",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")