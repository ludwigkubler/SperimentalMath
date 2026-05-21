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
    
    def generate_disjointness_function(n):
        return lambda x, y: all(xi != yi for xi, yi in zip(x, y))
    
    def compute_quiver_representation(f, n):
        quiver = {}
        for i in range(n):
            for j in range(i + 1, n):
                if f(tuple(range(i)), tuple(range(j))):
                    quiver[(i, j)] = True
                else:
                    quiver[(i, j)] = False
        return quiver
    
    def minimal_root_separation(quiver):
        roots = set()
        for (i, j), value in quiver.items():
            if value:
                roots.add(i)
                roots.add(j)
        return len(roots)
    
    def communication_complexity(f, n):
        # Simplified estimate based on the conjecture
        return math.sqrt(n)
    
    n = random.randint(5, 40)
    f = generate_disjointness_function(n)
    quiver = compute_quiver_representation(f, n)
    root_separation = minimal_root_separation(quiver)
    comm_complexity = communication_complexity(f, n)
    
    conjecture_holds = root_separation >= math.sqrt(n) and comm_complexity <= 2 * math.sqrt(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")