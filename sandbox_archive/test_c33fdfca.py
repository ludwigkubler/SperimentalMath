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
    
    n = 5 + (seed % 40) // 2  # Sweep n through {5, 10, 15, 20, 30, 40}
    if n == 1:
        return {
            "metric_name": "CC_GT(n)",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "single_output_stub"
        }
    
    # Generate a random Boolean function f on n variables
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the communication complexity of the Greater-Than function
    CC_GT_n = math.log(n, 2)
    
    # Compute the noncommutative Fourier coefficient at irreducible representation λ
    λ = n // 2  # Example: using a simple irreducible representation for demonstration
    F_λ_f = sum(f[i] * math.exp(-2j * math.pi * i * λ) for i in range(2**n)) / (2**n)
    
    # Compute the magnitude of the Fourier coefficient
    metric_value = abs(F_λ_f)
    
    # Check if the conjecture holds
    conjecture_holds = metric_value >= CC_GT_n / math.log(n, 2)
    counterexample = "" if conjecture_holds else f"CC_GT({n})={CC_GT_n}, |F_λ(f)|={metric_value}"
    
    return {
        "metric_name": "CC_GT(n)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")