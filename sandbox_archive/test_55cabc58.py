# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def parity_polynomial(n):
        return [sum(1 for i in range(n) if bin(i).count('1') % 2 == j) for j in range(2)]
    
    def real_dimension(poly, n):
        # This is a placeholder function. For simplicity, we assume the dimension is at least log₂(size(C))
        size_C = len(poly)
        return math.log2(size_C)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit_size = random.randint(1, 1 << n)  # Random AC⁰ circuit size
    poly = parity_polynomial(n)
    dim = real_dimension(poly, n)
    
    lower_bound = math.log2(circuit_size)
    
    return {
        "metric_name": "real_dimension",
        "metric_value": dim,
        "instances_tested": 1,
        "conjecture_holds": dim >= lower_bound,
        "counterexample": "" if dim >= lower_bound else f"dim={dim} < lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dim = sum(r["metric_value"] for r in results) / len(results)
    std_dim = math.sqrt(sum((r["metric_value"] - mean_dim) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dim} std={std_dim} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dim < lower_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")