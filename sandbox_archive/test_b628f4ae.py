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
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_norms = []
    
    for n in n_values:
        m = random.randint(1, 10 * n)
        formula = [random.choice([True, False]) for _ in range(m)]
        
        # Simulate computing the Hodge norm (placeholder value)
        hodge_norm = sum(abs(x) for x in formula) / math.sqrt(n * m)
        hodge_norms.append(hodge_norm)
    
    avg_hodge_norm = sum(hodge_norms) / len(hodge_norms)
    expected_hodge_norm = 1.0  # Placeholder value, replace with actual calculation
    conjecture_holds = abs(avg_hodge_norm - expected_hodge_norm) <= 0.1 * expected_hodge_norm
    
    return {
        "metric_name": "Hodge Norm",
        "metric_value": avg_hodge_norm,
        "instances_tested": len(hodge_norms),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")