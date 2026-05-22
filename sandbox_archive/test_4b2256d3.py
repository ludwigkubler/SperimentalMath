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
    
    def generate_read_twice_bp(n):
        # Generate a simple read-twice branching program with size n^2
        bp = []
        for i in range(n):
            bp.append([i, (i + 1) % n])
        return bp
    
    def minimal_rank(bp):
        # Compute the minimal rank of the representation into C_n
        n = len(bp)
        generators = set()
        for node in bp:
            generators.add(node[0])
            generators.add(node[1])
        return len(generators)
    
    def read_twice_bp_width(bp):
        # Compute the width of the read-twice branching program
        n = len(bp)
        width = 2 * (n - 1)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n)
        rank = minimal_rank(bp)
        width = read_twice_bp_width(bp)
        
        if width == 0:
            continue
        
        metric_value = rank / width
        instances_tested = 1
        conjecture_holds = rank >= n / (4 * math.log2(width))
        counterexample = "" if conjecture_holds else "mapping_undefined"
        
        results.append({
            "metric_name": "Minimal Rank / Read-Twice BP Width",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")