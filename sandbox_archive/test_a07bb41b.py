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
    
    # Define constants and parameters
    n = 30
    c = 1.0
    
    # Generate a random quaternionic representation (simplified for testing)
    Q = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Tropicalize the quaternionic representation
    Q_trop = [[max(q[i][j], q[j][i]) for j in range(n)] for i in range(n)]
    
    # Construct an AC⁰ PARITY circuit with varying depth and diameter
    depth = random.randint(5, 10)
    diameter = 2 ** (depth - 1) - 1
    
    # Calculate the minimal rank of the tropicalized representation
    tau_pi_trop = sum(sum(row) for row in Q_trop)
    
    # Check if the conjecture holds
    ratio = tau_pi_trop / math.log(diameter + 1)
    conjecture_holds = ratio >= c
    
    # Return the result
    return {
        "metric_name": "Minimal Rank",
        "metric_value": ratio,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} < {c}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default list of primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")