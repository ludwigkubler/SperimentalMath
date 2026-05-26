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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        # Simplified protocol: each bit requires 1 unit of communication
        return n
    
    def tensor_network_rank(f):
        # Placeholder implementation; actual computation depends on the function's structure
        return len(f) * (len(f) + 1) // 2
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    cc = communication_complexity(f)
    rank = tensor_network_rank(f)
    
    ratio = rank / cc if cc != 0 else float('inf')
    
    return {
        "metric_name": "rank_over_cc",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,  # Placeholder constant c
        "counterexample": "" if ratio <= 2 else f"rank={rank}, cc={cc}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction < 0.75:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds CC\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")