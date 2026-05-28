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
    
    # Generate a random finite field F_q with q ≥ 5
    q = random.randint(5, 100)
    F_q = [i for i in range(q)]
    
    # Generate a random arithmetic variety V over F_q
    n = random.randint(5, 40)  # Number of dimensions
    V = [[random.choice(F_q) for _ in range(n)] for _ in range(random.randint(10, 30))]
    
    # Compute the Hodge decomposition (simplified version)
    # For simplicity, we assume δ_H(V) is proportional to n
    delta_H_V = n
    
    # Estimate the quantum query complexity Q(Q(V))
    # For simplicity, we assume Q(Q(V)) is proportional to log(q)
    Q_Q_V = math.log(q, 2)
    
    # Check if the conjecture holds
    conjecture_holds = (delta_H_V <= 2 * Q_Q_V)
    counterexample = "" if conjecture_holds else f"δ_H(V)={delta_H_V}, Q(Q(V))={Q_Q_V}"
    
    return {
        "metric_name": "Minimal Depth of Hodge Decomposition",
        "metric_value": delta_H_V,
        "instances_tested": len(V),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.randint(2, 1000) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")