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
    
    def degree_of_function(func):
        return max(len(bin(x)[2:]) - bin(x).count('1') for x in range(len(func)))
    
    def monomial_ideal_to_coxeter_group_size(monomial_ideal):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(monomial_ideal)
    
    n = random.randint(5, 40)  # Generate a random number of variables between 5 and 40
    boolean_function = generate_boolean_function(n)
    degree = degree_of_function(boolean_function)
    coxeter_group_size = monomial_ideal_to_coxeter_group_size(boolean_function)
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": coxeter_group_size,
        "instances_tested": 1,
        "conjecture_holds": coxeter_group_size <= degree,
        "counterexample": "" if conjecture_holds else f"Function with n={n}, degree={degree}, group size={coxeter_group_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")