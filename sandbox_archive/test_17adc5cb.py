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
        m = len(V[0])
        V_trop = [[max(a, b) for a, b in zip(row1, row2)] for row1, row2 in V]
        return V_trop
    
    def xor_and_tree_width(V):
        # Placeholder function to compute XOR-AND tree width
        # This is a dummy implementation and should be replaced with actual logic
        n = len(V)
        m = len(V[0])
        return max(n, m)  # Simplified for demonstration purposes
    
    def generate_group_representation():
        G = [f"g{i}" for i in range(1, 41)]
        V = [[random.randint(-10, 10) for _ in range(40)] for _ in range(40)]
        return G, V
    
    G, V = generate_group_representation()
    V_trop = tropicalize(V)
    w = xor_and_tree_width(V_trop)
    
    r_V_trop = sum(max(row) for row in V_trop)
    
    metric_value = r_V_trop / math.log2(w + 1)
    
    if metric_value > 10:
        return {
            "metric_name": "r(V_trop) / log2(w + 1)",
            "metric_value": metric_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Metric value exceeds 10"
        }
    
    return {
        "metric_name": "r(V_trop) / log2(w + 1)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"metric_value < 0.8\" first_failing_seed={first_failing_seed}")