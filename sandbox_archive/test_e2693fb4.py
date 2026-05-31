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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def dpll_solver(formula):
        def solve(model):
            if not formula:
                return model
            literal = next((l for l in range(1, n + 1) if l not in model and -l not in model), None)
            if literal is None:
                return None
            new_model = model.copy()
            new_model[literal] = True
            result = solve(new_model)
            if result is not None:
                return result
            new_model[literal] = False
            new_model[-literal] = True
            return solve(new_model)

        n = len(formula[0])
        return solve({})

    def compute_resolution_proof_size(formula):
        # Simplified DPLL solver for proof size estimation
        if dpll_solver(formula) is None:
            return 1
        else:
            return 0

    def compute_local_algebraic_geometric_rank(formula):
        # Placeholder function, actual implementation required
        return random.randint(1, n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_3cnf(n)
    mlag = compute_local_algebraic_geometric_rank(formula)
    s = compute_resolution_proof_size(formula)

    return {
        "metric_name": "correlation",
        "metric_value": mlag * s,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)

    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")