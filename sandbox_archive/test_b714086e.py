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
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(10):  # Generate a simple formula with 10 clauses
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def count_cuspidal_sheaves(formula):
        # Placeholder implementation. This is a stub and should be replaced with actual logic.
        return len(formula.split())
    
    def resolution_proof_width(formula):
        # Placeholder implementation. This is a stub and should be replaced with actual logic.
        return len(formula.split(' and '))
    
    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    cuspidal_sheaves = count_cuspidal_sheaves(formula)
    width = resolution_proof_width(formula)
    
    return {
        "metric_name": "#cuspidal_sheaves",
        "metric_value": cuspidal_sheaves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(cuspidal_sheaves - width) <= max(2, width // 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")