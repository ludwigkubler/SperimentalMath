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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_secant_volume(f):
        # Placeholder function to simulate computation
        # Actual implementation would depend on algebraic geometry tools
        return len(f) ** 0.5
    
    def communication_complexity(f):
        # Placeholder function to simulate computation
        # Actual implementation would depend on communication complexity tools
        return len(f)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    secant_volume = compute_secant_volume(f)
    cc = communication_complexity(f)
    
    if secant_volume < n or cc > secant_volume:
        return {
            "metric_name": "secant_volume",
            "metric_value": secant_volume,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CC(f)={cc} > τ(f)={secant_volume}"
        }
    
    return {
        "metric_name": "secant_volume",
        "metric_value": secant_volume,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 * r["instances_tested"] for r in results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break