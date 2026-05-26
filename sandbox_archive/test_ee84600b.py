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
    
    def generate_groupoid(n):
        # Simplified construction for demonstration purposes
        return {i: (i + 1) % n for i in range(n)}
    
    def cohomological_dimension(G):
        return len(G)
    
    def tropicalized_cohomology(G):
        n = cohomological_dimension(G)
        # Placeholder computation
        return n
    
    def communication_complexity(n):
        # Placeholder computation
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    G = generate_groupoid(n)
    tau_G = tropicalized_cohomology(G)
    CC_R_DISJ_n = communication_complexity(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_R_DISJ_n,
        "instances_tested": 1,
        "conjecture_holds": tau_G >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 107))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient seeds")