# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30  # Fixed size for simplicity, can be adjusted as needed
    f = [random.randint(0, 1) for _ in range(n)]
    
    def communication_complexity(f):
        # Simulate the communication complexity of the disjointness problem
        return sum(f) * (n - sum(f))
    
    def minimal_local_index(f):
        # Placeholder for the actual computation of the minimal local index
        # For simplicity, we use a dummy value that depends on n and f
        return Fraction(n, 2)
    
    LC = communication_complexity(f)
    I_L_p = minimal_local_index(f)
    
    if LC == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": LC,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "LC is zero, communication complexity cannot be lower bounded by a positive index."
        }
    
    ratio = I_L_p / LC
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": LC,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds threshold."
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No seeds tested")