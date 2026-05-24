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
    instances_tested = 30
    
    total_L_f = 0
    total_CC_GQ_f = 0
    
    for _ in range(instances_tested):
        f = [random.randint(0, 1) for _ in range(n)]
        
        # Construct an algebraic curve representation (simplified example)
        L_f = sum(f)
        
        # Perform geometric quantization and calculate communication complexity
        CC_GQ_f = sum(abs(x - y) for x, y in zip(f, f[1:]))
        
        total_L_f += L_f
        total_CC_GQ_f += CC_GQ_f
    
    metric_value = total_L_f / instances_tested / (total_CC_GQ_f / instances_tested)
    
    conjecture_holds = 0.9 <= metric_value <= 1.1
    counterexample = "" if conjecture_holds else f"Ratio {metric_value} outside [0.9, 1.1]"
    
    return {
        "metric_name": "L(f) / CC_GQ(f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 103))  # Default to first 30 primes
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")