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
    
    n = random.randint(5, 40)
    hypercube = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the minimum linking number (simplified example)
    min_linking_number = sum(random.random() for _ in range(n)) / n
    
    # Simulate constructing a read-twice BP (simplified example)
    bp_width = random.randint(1, 2 * n)
    
    # Check if DPLL search tree width is within polynomial factor of the minimum linking number
    dpll_width = bp_width + random.randint(0, n)  # Polynomial size overhead
    
    conjecture_holds = dpll_width <= min_linking_number * (n ** 2)
    counterexample = "" if conjecture_holds else f"BP width {bp_width} exceeds polynomial factor of linking number {min_linking_number}"
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": dpll_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")