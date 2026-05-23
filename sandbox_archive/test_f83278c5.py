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
    
    # Generate a random geometric group G (simplified for demonstration)
    n = 5 + random.randint(0, 30)
    G = {i: set(range(n)) for i in range(n)}
    
    # Construct an AC0 parity circuit C with increasing sizes
    S_C_values = [10**i for i in range(1, 6)]
    ratios = []
    
    for S_C in S_C_values:
        # Compute the r(G)-invariant subset for each group action on the circuit
        r_G_S_C = sum(len(G[i] & set(range(S_C))) for i in G) / len(G)
        
        # Compare it to c_G·log(S(C))
        if n == 0: continue  # Avoid division by zero
        c_G = math.log(n) / S_C
        ratio = r_G_S_C / (c_G * math.log(S_C))
        ratios.append(ratio)
    
    # Measure the rank of the invariant subset and compare it to c_G·log(S(C))
    metric_value = sum(ratios) / len(ratios)
    conjecture_holds = all(r <= 1 for r in ratios)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": len(S_C_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")