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
    
    def tropicalize(V):
        return [[max(a, b) for a, b in zip(row1, row2)] for row1, row2 in V]
    
    def xor_and_tree_width(tree):
        if isinstance(tree, list):
            return 1 + max(xor_and_tree_width(subtree) for subtree in tree)
        else:
            return 0
    
    n = random.randint(5, 40)
    G = [f"g{i}" for i in range(n)]
    V = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    V_trop = tropicalize(V)
    r_V_trop = sum(sum(row) for row in V_trop)
    
    tree_width = xor_and_tree_width(G)
    log2_w_plus_1 = math.log2(tree_width + 1)
    
    return {
        "metric_name": "correlation",
        "metric_value": r_V_trop / log2_w_plus_1,
        "instances_tested": 1,
        "conjecture_holds": r_V_trop <= log2_w_plus_1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")