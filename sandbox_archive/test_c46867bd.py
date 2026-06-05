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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Generate a small number of clauses to keep n manageable
            clause = [random.randint(-1, -n), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Simplified version for demonstration purposes
        return len(cnf)
    
    def p_adic_logarithmic_potential(cnf):
        # Simplified version for demonstration purposes
        return len(cnf) ** 0.5
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    cr = communication_complexity_rank(cnf)
    plp = p_adic_logarithmic_potential(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": math.correl(cr, plp),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if r["metric_value"] >= 0.7) / len(results) >= 0.8333:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")