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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_width(f):
        n = len(f)
        width = 0
        for i in range(n):
            if f[i] == 1:
                width += 1
        return width
    
    def compute_free_probability_space_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    width = compute_width(f)
    rank_free_prob = compute_free_probability_space_rank(f)
    
    if width == 0:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "width_undefined"
        }
    
    ratio = rank_free_prob / math.log(width)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": "" if 0.5 <= ratio <= 2 else f"ratio_out_of_bounds: {ratio}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r and r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")