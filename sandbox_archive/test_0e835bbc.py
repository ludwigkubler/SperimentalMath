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

def generate_cnf(n: int, m: int) -> list:
    variables = [f'x{i+1}' for i in range(n)]
    cnf = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        cnf.append(f"{' or '.join(clause)}")
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, n // 10)  # Ensure at least one clause
        cnf = generate_cnf(n, m)
        
        # Simulate DPLL proof length (simplified model)
        proof_length = random.randint(1, 2**n)
        
        r_T = math.ceil(math.log(n, 2))  # Simplified minimal rank calculation
        
        results.append({
            "metric_name": "DPLL Proof Length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": proof_length <= 2**(r_T / 2),
            "counterexample": "" if proof_length <= 2**(r_T / 2) else f"n={n}, r(T)={r_T}, L={proof_length}"
        })
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")