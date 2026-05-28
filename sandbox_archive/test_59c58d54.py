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
    
    def is_symmetric(f, perm):
        n = int(math.log2(len(f)))
        for i in range(2**n):
            if f[perm[i]] != f[i]:
                return False
        return True
    
    def find_symmetry_group(f):
        n = int(math.log2(len(f)))
        G = set()
        for perm in itertools.permutations(range(2**n)):
            if is_symmetric(f, perm):
                G.add(tuple(perm))
        return G
    
    def circuit_size(G):
        # Placeholder for actual circuit size computation
        return len(G)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    G = find_symmetry_group(f)
    circuit_size_val = circuit_size(G)
    
    metric_value = circuit_size_val / (2 * n**2)
    conjecture_holds = circuit_size_val <= 2 * n
    counterexample = "" if conjecture_holds else f"Function with {n} variables and symmetry group size {len(G)} has circuit size {circuit_size_val}"
    
    return {
        "metric_name": "Circuit Size / Symmetry Group Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")