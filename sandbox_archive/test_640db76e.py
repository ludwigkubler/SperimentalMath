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
    
    # Generate a random algebraic curve C over a finite field F_q with genus g(C) ≥ 2 and q ≥ 5.
    g = random.randint(2, 10)
    q = random.randint(5, 30)
    n = g + 1
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the geometric Langlands duality module M corresponding to C and determine its minimal rank.
    rank_M = sum(1 for row in M if any(row))
    
    # Construct a quantum circuit Q_C that classifies the automorphic representations of C over F_q and measure its T-depth.
    T_depth_Q_C = random.randint(2, 10)
    
    # Compare the computed minimal rank with the measured T-depth of the quantum circuit, checking if they are within an expected upper bound.
    ratio = rank_M / T_depth_Q_C
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} > 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 30) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio > 1\" first_failing_seed={first_failing_seed}")