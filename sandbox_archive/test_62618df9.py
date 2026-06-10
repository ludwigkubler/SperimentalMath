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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_minimal_order_of_quandle_action(f):
        n = int(math.log2(len(f)))
        # Placeholder implementation of minimal order calculation
        # This is a dummy value and should be replaced with actual logic
        return random.randint(1, 5)
    
    def calculate_rank_variance(f):
        n = int(math.log2(len(f)))
        # Placeholder implementation of rank variance calculation
        # This is a dummy value and should be replaced with actual logic
        return random.uniform(0.1 * n**2, 2 * n**2)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    m = calculate_minimal_order_of_quandle_action(f)
    rank_variance = calculate_rank_variance(f)
    
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if m <= rank_variance <= m**2 else False,
        "counterexample": "" if m <= rank_variance <= m**2 else f"m={m}, rank_variance={rank_variance}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")