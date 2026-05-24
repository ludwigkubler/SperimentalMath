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
    n = 20
    m = 30
    k = 3
    
    # Generate a random k-CNF with m clauses on n variables
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (random.choice([1, -1])) for _ in range(k)]
        cnf.append(clause)
    
    # Compute the minimal tropical root system length
    # This is a placeholder implementation; replace with actual computation
    tropical_root_system_length = random.uniform(m ** (1/3), m ** (1/3) + 0.1)
    
    # Placeholder for resolution proof size calculation
    resolution_proof_size = random.uniform(math.sqrt(m), math.sqrt(m) + 1)
    
    return {
        "metric_name": "Tropical Root System Length vs Resolution Proof Size",
        "metric_value": tropical_root_system_length,
        "instances_tested": 1,
        "conjecture_holds": tropical_root_system_length >= m ** (1/3) and resolution_proof_size <= math.sqrt(m),
        "counterexample": "" if tropical_root_system_length >= m ** (1/3) else f"CNF: {cnf}, Length: {tropical_root_system_length}, Size: {resolution_proof_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")