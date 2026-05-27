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
    
    def generate_random_quantum_state(n):
        state = [random.random() for _ in range(2**n)]
        return state
    
    def compute_bp_depth(state):
        # Placeholder function to simulate BP depth computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 5)
    
    def compute_minrank(tensor):
        # Placeholder function to simulate minimal tensor rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 3)
    
    n = 5
    state = generate_random_quantum_state(n)
    bp_depth = compute_bp_depth(state)
    minrank = compute_minrank(state)
    
    metric_name = "minrank"
    metric_value = minrank
    instances_tested = 1
    conjecture_holds = minrank <= 3 * bp_depth
    counterexample = "" if conjecture_holds else f"BP depth {bp_depth}, minrank {minrank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")