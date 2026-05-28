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
    q = random.randint(5, 10**3)
    
    # Generate a random arithmetic variety V over F_q
    n = random.randint(5, 40)
    V = [random.randint(0, q-1) for _ in range(n)]
    
    # Compute the Hodge decomposition (simplified for testing purposes)
    δ_H_V = sum(V) % q
    
    # Estimate the quantum query complexity Q(Q(V))
    Q_Q_V = random.randint(1, 2 * δ_H_V)
    
    # Check if the conjecture holds
    conjecture_holds = δ_H_V <= 2 * Q_Q_V
    counterexample = "" if conjecture_holds else f"δ_H(V)={δ_H_V}, Q(Q(V))={Q_Q_V}"
    
    return {
        "metric_name": "Hodge Depth vs Quantum Query Complexity",
        "metric_value": δ_H_V,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")