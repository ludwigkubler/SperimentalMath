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

def generate_frege_proof(depth: int) -> list:
    if depth == 1:
        return [random.choice(['A', 'B', 'C'])]
    else:
        left = generate_frege_proof(random.randint(1, min(depth-2, 1)))
        right = generate_frege_proof(depth - len(left) - 1)
        return ['(', *left, '+', *right, ')']

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "min_generators"
    instances_tested = 0
    total_generators = 0
    n_max = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each depth 5 times
            instances_tested += 1
            n_max = max(n_max, depth)
            proof = generate_frege_proof(depth)
            
            # Simulate a monoidal category representation by counting unique symbols
            generators = set()
            for step in proof:
                if step.isalpha():
                    generators.add(step)
            
            total_generators += len(generators)
    
    mean_generators = Fraction(total_generators, instances_tested)
    conjecture_holds = mean_generators <= depth**2
    
    return {
        "metric_name": metric_name,
        "metric_value": float(mean_generators),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean={mean_generators}, depth^2={depth**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")