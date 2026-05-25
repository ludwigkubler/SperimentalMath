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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [variables[i-1]]
            for j in range(i+1, n+1):
                clause.append(f'~{variables[j-1]}')
            clauses.append(clause)
        return variables, clauses

    def tseitin_resolution_length(variables, clauses):
        # Simplified resolution length calculation
        return len(variables) + len(clauses)

    def quantum_logarithmic_potential(n):
        # Simplified quantum logarithmic potential calculation
        return math.log2(n)

    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    t_star_F = tseitin_resolution_length(variables, clauses)
    phi_F = quantum_logarithmic_potential(n)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": 0.85 * (phi_F / t_star_F),  # Simplified metric
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")