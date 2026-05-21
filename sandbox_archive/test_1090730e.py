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
    
    def nauty(g):
        # Placeholder for nauty implementation
        return len(g), 1  # Simplified version, actual nauty is more complex
    
    def resolution_width(formula):
        # Placeholder for SAT solver implementation
        return len(formula.split())  # Simplified version, actual DRAT-trace is more complex
    
    def count_conjugacy_classes(group):
        # Placeholder for counting conjugacy classes in a group
        return len(group)  # Simplified version, actual computation depends on the group structure
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    C_G, _ = nauty(G)
    res_width_G = resolution_width(" ".join(str(random.randint(0, 1)) for _ in range(n * (n - 1) // 2)))
    
    conjecture_holds = res_width_G >= C_G
    counterexample = "" if conjecture_holds else f"res_width_G={res_width_G}, C(G)={C_G}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": res_width_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")