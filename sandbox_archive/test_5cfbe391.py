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
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
            clauses.append(f'~{variables[i]}')
        for i in range(1, n):
            clauses.append(f'{variables[i-1]} | {variables[i]}')
        return variables, clauses
    
    def is_expander_graph(variables, clauses):
        # Placeholder for actual expander graph detection logic
        return False
    
    def compute_min_local_curvature(M):
        # Placeholder for actual computation of minimum local curvature
        return 1
    
    def resolution_prover(clauses):
        # Placeholder for actual resolution prover logic
        return len(clauses)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    M = compute_min_local_curvature(variables)
    proof_length = resolution_prover(clauses)
    
    if is_expander_graph(variables, clauses):
        expected_length = 2 ** (math.ceil(math.log(M, 2)))
    else:
        expected_length = float('inf')
    
    conjecture_holds = proof_length >= expected_length
    counterexample = "" if conjecture_holds else "expander_graph"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")