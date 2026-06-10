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
    
    def poincare_disk_volume(n):
        if n == 1:
            return 0.5 * math.pi
        volume = 0
        for _ in range(1000):  # Sample 1000 points to estimate the volume
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            if x**2 + y**2 < 1:
                volume += math.log(1 - (x**2 + y**2))
        return -volume / n
    
    def hyperbolic_volume(n):
        return poincare_disk_volume(n) * n
    
    volumes = []
    for _ in range(30):  # Test on 30 instances
        n = random.choice([5, 10, 15, 20, 30, 40])
        volume = hyperbolic_volume(n)
        if volume <= 0:
            return {
                "metric_name": "hyperbolic_volume",
                "metric_value": -1,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "volume_non_positive"
            }
        volumes.append(volume)
    
    mean = sum(volumes) / len(volumes)
    std_dev = math.sqrt(sum((x - mean)**2 for x in volumes) / len(volumes))
    conjecture_holds = 0.5 <= mean / (1 / math.sqrt(len(volumes))) <= 2 and max(volumes) <= 3 * (1 / math.sqrt(len(volumes)))
    
    return {
        "metric_name": "hyperbolic_volume",
        "metric_value": mean,
        "instances_tested": len(volumes),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "volume_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")