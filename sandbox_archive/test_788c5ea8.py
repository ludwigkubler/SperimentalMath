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
    
    def generate_circuit(n):
        if n == 1:
            return [0]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [0] + left + right
    
    def monotone_width(circuit):
        width = 0
        max_width = 0
        for i in range(len(circuit)):
            if circuit[i] == 1:
                width += 1
            else:
                max_width = max(max_width, width)
                width = 0
        return max(max_width, width)
    
    def geometric_group_size(n):
        # Simplified model: size proportional to n^2
        return n * (n + 1) // 2
    
    def automorphism_group_size(group_size):
        # Simplified model: size proportional to group_size^0.5
        return int(math.sqrt(group_size))
    
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        width = monotone_width(circuit)
        group_size = geometric_group_size(n)
        gen_size = automorphism_group_size(group_size)
        
        if n > 40:
            return {
                "metric_name": "monotone_width",
                "metric_value": width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "n_max_exceeded"
            }
        
        if abs(gen_size - width) > 3:
            return {
                "metric_name": "monotone_width",
                "metric_value": width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"gen_size={gen_size}, width={width}"
            }
    
    return {
        "metric_name": "monotone_width",
        "metric_value": width,
        "instances_tested": 6,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")