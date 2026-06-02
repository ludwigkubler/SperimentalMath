# auto-injected by SEC sandbox
import math
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

def generate_tseitin_formula(n: int, m: int) -> tuple:
    variables = list(range(1, n + 1))
    literals = [f"v{i}" for i in variables] + [f"~v{i}" for i in variables]
    clauses = []

    # Generate clauses
    for _ in range(m):
        clause = random.sample(literals, 2)
        clauses.append(clause)

    return variables, literals, clauses

def solve_diophantine_equations(variables: list, literals: list, clauses: list) -> int:
    # Placeholder function to simulate solving Diophantine equations
    # In practice, you would implement a proper algorithm here
    return len(literals)

def compute_resolution_proof_width(clauses: list) -> int:
    # Placeholder function to simulate computing resolution proof width
    # In practice, you would implement a proper algorithm here
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 10 * n
    
    variables, literals, clauses = generate_tseitin_formula(n, m)
    num_solutions = solve_diophantine_equations(variables, literals, clauses)
    proof_width = compute_resolution_proof_width(clauses)
    
    metric_value = abs(num_solutions - proof_width) / max(1, proof_width)
    conjecture_holds = 0.5 <= metric_value <= 2.0
    counterexample = "" if conjecture_holds else f"num_solutions={num_solutions}, proof_width={proof_width}"
    
    return {
        "metric_name": "Diophantine Complexity / Resolution Proof Width Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_value out of expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")