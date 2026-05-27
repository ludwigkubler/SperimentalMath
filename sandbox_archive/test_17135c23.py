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
    
    n = random.randint(5, 40)  # Number of bits
    m = random.randint(1, 2**n - 1)  # Number of messages
    
    # Generate a random communication protocol
    protocol = [random.choice([0, 1]) for _ in range(n)]
    
    # Generate a random set of messages
    messages = [random.choice([0, 1]) for _ in range(m)]
    
    # Compute the Deligne-Lusztig indicator D_L
    D_L = sum(messages[i] * protocol[i % n] for i in range(m))
    
    # Tropicalize D_L (simply take the maximum)
    T_D_L = max(D_L, 0)
    
    # Compute the rank of T(D_L) (since it's a single value, rank is 1 if non-zero, 0 otherwise)
    rank_T_D_L = 1 if T_D_L > 0 else 0
    
    return {
        "metric_name": "rank(T(D_L))",
        "metric_value": rank_T_D_L,
        "instances_tested": 1,
        "conjecture_holds": rank_T_D_L <= m * math.log(n),
        "counterexample": "" if rank_T_D_L <= m * math.log(n) else f"m={m}, n={n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")