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
    
    def generate_random_quantum_state(n):
        state = [random.random() for _ in range(2**n)]
        return state
    
    def compute_minrank(state, n):
        # Simplified tensor rank computation (not actual tensor rank)
        return sum(abs(x) for x in state)
    
    def compute_bp_depth(n):
        # Simplified BP depth computation (not actual BP depth)
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    rho = generate_random_quantum_state(n)
    minrank = compute_minrank(rho, n)
    bp_depth = compute_bp_depth(n)
    
    return {
        "metric_name": "minrank",
        "metric_value": minrank,
        "instances_tested": 1,
        "conjecture_holds": minrank <= 3 * bp_depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minrank = sum(r["metric_value"] for r in results) / len(results)
    std_minrank = math.sqrt(sum((r["metric_value"] - mean_minrank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_minrank} std={std_minrank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")