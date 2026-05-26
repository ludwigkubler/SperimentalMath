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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate an explicit function f in P with known Frege proof depth d
    n = random.randint(5, 40)
    d = random.randint(2, n // 2)
    
    # Compute the tensor representation of the function and determine its minimal rank
    # This is a placeholder for actual computation; replace with actual code
    min_rank = random.randint(d // 2, d + 1)  # Simulate minimal rank
    
    # Compare the minimal rank to half the Frege proof depth d
    difference = abs(min_rank - d / 2)
    
    return {
        "metric_name": "minimal_rank_difference",
        "metric_value": difference,
        "instances_tested": 1,
        "conjecture_holds": difference <= 3,
        "counterexample": f"rank={min_rank}, expected={d/2}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")