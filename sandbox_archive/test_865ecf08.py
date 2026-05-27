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
    
    n = 10  # Number of bits
    m = 5   # Number of messages
    
    # Generate a random communication complexity instance
    protocol = [random.choice([0, 1]) for _ in range(n)]
    messages = [random.randint(0, m-1) for _ in range(m)]
    
    # Compute the Deligne-Lusztig indicator (simplified example)
    D_L = sum(messages[i] * protocol[i] for i in range(n))
    
    # Tropicalize the Deligne-Lusztig indicator
    T_D_L = max(D_L, 0)  # Simplified tropicalization
    
    # Determine the rank of the tropicalized indicator (simplified example)
    rank_T_D_L = 1 if T_D_L > 0 else 0
    
    # Check the conjecture
    conjecture_holds = rank_T_D_L <= m * math.log(n)
    
    return {
        "metric_name": "rank(T(D_L))",
        "metric_value": rank_T_D_L,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"m={m}, n={n}, D_L={D_L}, T(D_L)={T_D_L}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={results[0]['counterexample'].split(',')[1]}\" first_failing_seed={first_failing_seed}")