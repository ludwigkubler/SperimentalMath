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
    
    def generate_3cnf(n, m):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 3)
            clauses.append(f"({' or '.join(clause)})")
        return ' and '.join(clauses)

    def continued_fraction_representation(formula):
        # Simplified representation for demonstration
        return len(formula.split(' and '))

    def rank_of_multivariate_cf(cf):
        # Rank is the number of variables in the simplest form
        return sum(1 for var in cf if var.startswith('x'))

    def min_resolution_proof_length(formula):
        # Dummy implementation for demonstration
        return 10 / len(formula.split(' and '))

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    formula = generate_3cnf(n, m)
    
    cf_representation = continued_fraction_representation(formula)
    rank = rank_of_multivariate_cf(cf_representation)
    proof_length = min_resolution_proof_length(formula)
    
    metric_value = rank / proof_length
    conjecture_holds = 0.8 <= metric_value <= 10
    
    return {
        "metric_name": "Rank/Proof Length Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula: {formula}, Rank: {rank}, Proof Length: {proof_length}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")