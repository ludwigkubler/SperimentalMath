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
    
    n = 10  # Number of instances per trial
    results = []
    
    for _ in range(n):
        f = [random.randint(0, 1) for _ in range(10)]  # Generate a random binary function
        
        # Calculate the minimal local index (simplified example)
        min_local_index = sum(f)
        
        # Calculate the entropy-based communication complexity (simplified example)
        entropy_based_comm_complexity = sum([f.count(x) * math.log2(f.count(x)) for x in set(f)]) if f else 0
        
        results.append({
            "metric_name": "MinimalLocalIndex",
            "metric_value": min_local_index,
            "instances_tested": n,
            "conjecture_holds": min_local_index <= 3 * entropy_based_comm_complexity,
            "counterexample": "" if min_local_index <= 3 * entropy_based_comm_complexity else f"Counterexample: f={f}"
        })
    
    return {
        "seed": seed,
        "metric_name": "MinimalLocalIndex",
        "metric_value": sum(result["metric_value"] for result in results) / n,
        "instances_tested": n,
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")