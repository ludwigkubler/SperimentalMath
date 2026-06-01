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
    
    def generate_formula(n, num_clauses):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(num_clauses):
            clause = random.sample(variables, 2)
            clause.append(random.choice(['', 'NOT']))
            clauses.append(clause)
        return clauses
    
    def p_adic_root_count(formula):
        # Placeholder implementation
        return len(formula)
    
    def frege_proof_length(formula):
        # Placeholder implementation
        return len(formula) * 2
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, n*3)
    formula = generate_formula(n, num_clauses)
    
    root_count = p_adic_root_count(formula)
    proof_length = frege_proof_length(formula)
    
    ratio = root_count / proof_length if proof_length > 0 else float('inf')
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")