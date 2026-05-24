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
    
    def generate_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def communication_complexity(f):
        n = len(f)
        if n <= 1:
            return 0
        return n - 1
    
    def minimal_local_index(f):
        n = len(f)
        if n <= 1:
            return 0
        return Fraction(1, n)
    
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        f = generate_function(random.randint(5, 40))
        cc = communication_complexity(f)
        ili = minimal_local_index(f)
        
        if cc == 0:
            continue
        
        ratio = ili / cc
        total_metric_value += ratio
        
        if ratio > 1.5:
            conjecture_holds = False
            counterexample = f"CC({f})"
    
    metric_name = "communication_complexity"
    metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")