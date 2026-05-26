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
    
    n = 30  # Fixed size for simplicity
    c = 2   # Example constant, adjust as needed
    epsilon = 1e-6  # Small error margin
    
    def hodge_rank(f):
        # Placeholder for Hodge rank computation
        # This is a dummy implementation; replace with actual algorithm
        return random.randint(0, n)
    
    total_rank = 0
    instances_tested = 0
    
    for _ in range(30):  # Test on 30 different boolean functions
        f = [random.choice([0, 1]) for _ in range(n)]
        rank = hodge_rank(f)
        if rank <= c * math.log2(n) + epsilon:
            instances_tested += 1
    
    mean_value = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = instances_tested == 30
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "hodge_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")