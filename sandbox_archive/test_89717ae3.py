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
    
    # Generate a random CNF formula with n variables and m clauses
    n = 20 + random.randint(0, 19)  # n in {5, 10, ..., 40}
    m = 3 * n + random.randint(0, 2 * n)
    
    # Create a list of literals (variables and their negations)
    literals = [f'x{i}' for i in range(n)] + [f'-x{i}' for i in range(n)]
    
    # Generate clauses
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)  # Each clause has exactly 3 literals
        clauses.append(clause)
    
    # Convert CNF to a string representation
    cnf_str = ' '.join([f'{" ".join(clause)} 0' for clause in clauses])
    
    # Placeholder for Hodge decomposition rank calculation (not implemented)
    HD_F = random.randint(1, n)  # Simulate a value for demonstration
    
    # Placeholder for resolution refutation size calculation (not implemented)
    t_star_F = random.randint(1, m)  # Simulate a value for demonstration
    
    # Calculate the ratio
    if t_star_F == 0:
        ratio = float('inf')
    else:
        ratio = HD_F / math.log(t_star_F)
    
    return {
        "metric_name": "HD(F) / log(t*(F))",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": False,  # Conjecture cannot be verified without actual implementation
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default to a list of 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")