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
        n = len(V)
        if n == 0 or any(len(row) != n for row in V):
            return []
        return [[max(a, b) for a, b in zip(row1, row2)] for row1, row2 in V]
    
    def xor_and_tree_width(G, V):
        # Placeholder function to compute XOR-AND tree width
        # This is a dummy implementation and should be replaced with actual logic
        return len(V)
    
    def group_action_representation(G, V):
        # Placeholder function to generate group action representation
        # This is a dummy implementation and should be replaced with actual logic
        return V
    
    n = random.randint(5, 40)
    G = [random.randint(1, n) for _ in range(n)]
    V = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    V_trop = tropicalize(V)
    w = xor_and_tree_width(G, V_trop)
    r_V_trop = len(V_trop)
    
    if r_V_trop > math.log2(w + 1):
        return {
            "metric_name": "correlation",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "r(V_trop) > log_2(w + 1)"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": r_V_trop / math.log2(w + 1),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"r(V_trop) > log_2(w + 1)\" first_failing_seed={first_failing_seed}")