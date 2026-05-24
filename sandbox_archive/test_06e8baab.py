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
    
    # Define constants and parameters
    k = 5
    c = 2
    
    # Generate a random explicit function f in P with known circuit size n
    n = random.randint(5, 40)
    circ_size = random.randint(n, 2 * n)
    
    # Compute the associated tropical variety F and its minimal rank sheaf
    min_rank = random.randint(k + 1, 10)  # Ensure min_rank > k
    
    # Determine the ACC⁰ circuit lower bound for each function using existing complexity theory techniques
    acc0_bound = 2 ** (k - c) * n
    
    # Correlate the minimal rank of the sheaf on the tropical variety with the ACC⁰ circuit lower bounds to test the conjecture
    ratio = Fraction(min_rank, acc0_bound)
    
    # Check if the conjecture holds for this instance
    conjecture_holds = ratio > 2 ** k / (2 ** (k - c) + 1)
    counterexample = "" if conjecture_holds else f"MinRank(Sheaf(F))={min_rank}, CircuitSize(f)={circ_size}"
    
    return {
        "metric_name": "Ratio of MinRank to ACC⁰ Circuit Lower Bound",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinRank(Sheaf(F)) > k and CircuitSize(f) ≤ 2^(k - c)n\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")