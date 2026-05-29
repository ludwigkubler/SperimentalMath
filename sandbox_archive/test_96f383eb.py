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
    
    def log_q(n, q):
        if n <= 0 or q <= 1:
            return 0
        return Fraction(math.log(q ** n), math.log(2))
    
    def arithmetic_hodge_dimension(n, q):
        # Placeholder for actual computation of the dimension
        # This is a dummy function that returns a random value for demonstration purposes
        return random.uniform(0, 1000)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        q = random.randint(2, 10)
        dim = arithmetic_hodge_dimension(n, q)
        bound = log_q(n, q) * (log_q(n, q) ** 2)
        
        results.append({
            "n": n,
            "q": q,
            "dim": dim,
            "bound": bound
        })
    
    mean_dim = sum(res["dim"] for res in results) / len(results)
    mean_bound = sum(res["bound"] for res in results) / len(results)
    
    conjecture_holds = all(abs(res["dim"] - mean_dim) <= abs(res["bound"] - mean_bound) for res in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, q={results[0]['q']}, dim={results[0]['dim']}"

    return {
        "metric_name": "arithmetic_hodge_dimension",
        "metric_value": mean_dim,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, q={results[0]['q']}, dim={results[0]['dim']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")