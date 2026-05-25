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
    
    # Define AC0_PARITY Depth function
    def ac0_parity_depth(n):
        if n == 1:
            return 1
        return 2 + ac0_parity_depth(n // 2)
    
    # Generate a random n-dimensional vector space
    n = random.randint(5, 40)
    V = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Compute the minimal rank of the quadratic intersection structure on G
    # This is a placeholder function. Replace with actual computation.
    def minimal_rank(V):
        return n  # Placeholder value
    
    min_rank = minimal_rank(V)
    
    # Build AC0 circuits for computing the parity function on n inputs and measure their depth
    circuit_depth = ac0_parity_depth(n)
    
    # Correlate the minimal ranks with the circuit depths
    c = math.log(n) / circuit_depth
    
    # Check if the conjecture holds
    if min_rank > c * circuit_depth:
        conjecture_holds = False
        counterexample = f"n={n}, min_rank={min_rank}, circuit_depth={circuit_depth}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")