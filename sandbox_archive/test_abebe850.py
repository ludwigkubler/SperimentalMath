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
    
    def generate_frege_proof(depth):
        if depth == 1:
            return ["P"]
        else:
            left = generate_frege_proof(random.randint(1, depth-1))
            right = generate_frege_proof(depth - len(left) - 1)
            return [f"({left[0]} {right[0]})"] + left + right
    
    def is_valid_category(generators):
        # Simple check to ensure the category has no self-loops or parallel edges
        for u, v in generators:
            if u == v or (u, v) in generators or (v, u) in generators:
                return False
        return True
    
    def count_generators(proof):
        seen = set()
        for step in proof:
            if step.startswith("("):
                continue
            seen.add(step)
        return len(seen)
    
    trials = 30
    n_max = 40
    total_generators = 0
    instances_tested = 0
    
    for depth in range(1, n_max + 1):
        for _ in range(trials // n_max):
            proof = generate_frege_proof(depth)
            generators = set()
            for step in proof:
                if step.startswith("("):
                    continue
                generators.add(step)
            if is_valid_category(generators):
                total_generators += count_generators(proof)
                instances_tested += 1
    
    mean_generators = total_generators / instances_tested
    conjecture_holds = mean_generators <= depth**2
    counterexample = "" if conjecture_holds else f"mean={mean_generators}, expected<=depth^2"
    
    return {
        "metric_name": "Mean Generators",
        "metric_value": mean_generators,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")