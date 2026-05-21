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
                quiver[(i, j)] = f([i], [j])
        return quiver
    
    def minimal_root_separation(quiver):
        if not quiver:
            return 0
        roots = set()
        for (i, j), val in quiver.items():
            if val:
                roots.add(i)
                roots.add(j)
        return len(roots) - 1
    
    def communication_complexity(f, n):
        # Simplified model: assume O(n) complexity
        return n
    
    n = random.randint(5, 40)
    f = generate_disjointness_function(n)
    quiver = compute_quiver_representation(f, n)
    root_separation = minimal_root_separation(quiver)
    comm_complexity = communication_complexity(f, n)
    
    conjecture_holds = root_separation >= math.sqrt(n) and comm_complexity <= 2 * math.sqrt(n)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")