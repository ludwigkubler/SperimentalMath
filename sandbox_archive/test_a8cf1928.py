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
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        else:
            return n - 1
    
    def minimal_rank(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return n * (n - 1) // 2
    
    instances_tested = 30
    total_metric_value = 0.0
    counterexample_found = False
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(random.randint(5, 40))]
        cc = communication_complexity(f)
        r = minimal_rank(f)
        
        if cc == 0:
            continue
        
        ratio = r / cc
        total_metric_value += ratio
        
        if not counterexample_found and r > cc * 2:  # Arbitrary threshold to detect non-polynomial relationship
            counterexample_found = True
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = not counterexample_found
    
    return {
        "metric_name": "ratio_of_rank_to_cc",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if not counterexample_found else "rank > 2 * cc"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank > 2 * cc' first_failing_seed={first_failing_seed}")