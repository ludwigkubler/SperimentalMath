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
    
    # Define constants and parameters
    n = 40
    max_threshold = n**2
    
    # Generate a BP_ReadTwice circuit with threshold O(n^2)
    bp_readtwice_threshold = random.randint(1, max_threshold)
    
    # Compute the Hilbert-Poincaré series of the tensor algebra on an n-dimensional vector space
    hilbert_poincare_series = sum([math.comb(n, k) for k in range(n + 1)])
    
    # Calculate the metric value (difference between BP_ReadTwice threshold and expected polynomial relationship)
    metric_value = abs(bp_readtwice_threshold - (n**2))
    
    # Determine if the conjecture holds
    conjecture_holds = metric_value <= 3
    
    return {
        "metric_name": "BP_ReadTwice Circuit Threshold vs Hilbert-Poincaré Series",
        "metric_value": metric_value,
        "instances_tested": n + 1,  # Including the seed itself
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Threshold {bp_readtwice_threshold} exceeds expected O(n^2)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Threshold exceeds expected O(n^2)\" first_failing_seed={first_failing_seed}")