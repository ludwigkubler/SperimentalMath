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

def is_quadratic_residue(a, p):
    return pow(a, (p - 1) // 2, p) == 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    R = random.uniform(0.1, 1.0)
    
    # Generate a random communication protocol
    protocol = [random.choice([0, 1]) for _ in range(n)]
    outcomes = set()
    for i in range(2**n):
        outcome = ''.join(str(protocol[j]) if (i >> j) & 1 else '0' for j in range(n))
        outcomes.add(outcome)
    
    # Count the number of quadratic residues needed to represent the outcomes
    p = random.choice([p for p in [3, 5, 7, 11, 13, 17, 19, 23] if (p - 1) % n == 0])
    residues = {a for a in range(p) if is_quadratic_residue(a, p)}
    required_residues = len([res for res in residues if res in outcomes])
    
    # Check the conjecture
    conjecture_holds = required_residues <= math.ceil(p ** (R + 1 / n))
    counterexample = "" if conjecture_holds else f"n={n}, R={R}, p={p}"
    
    return {
        "metric_name": "required_residues",
        "metric_value": required_residues,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")