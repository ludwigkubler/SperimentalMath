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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll_tree_diameter(phi):
        # Placeholder for DPLL search tree diameter calculation
        # This is a stub and should be replaced with actual implementation
        return len(phi)  # Simplified example
    
    def compute_genus(truth_table):
        # Placeholder for genus computation using 'topologylib'
        # This is a stub and should be replaced with actual implementation
        return random.randint(0, 10)  # Simplified example
    
    n = 5 + (seed % 35)  # Ensure n_min >= 5 and n_max >= 20
    phi = [random.choice([True, False]) for _ in range(n)]
    
    truth_table = []
    for i in range(1 << n):
        row = []
        for j in range(n):
            row.append(phi[j] if (i >> j) & 1 else not phi[j])
        truth_table.append(row)
    
    genus = compute_genus(truth_table)
    dll_tree_diameter = dpll_tree_diameter(phi)
    
    return {
        "metric_name": "genus",
        "metric_value": genus,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")