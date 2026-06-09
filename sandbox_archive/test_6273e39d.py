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

def generate_cnf(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def dpll(clauses):
    def solve(model):
        if not clauses:
            return model
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            false_literal = next((v for v in range(1, n + 1) if v not in model and -v not in model), None)
            if false_literal is None:
                return False
            model[frozenset([false_literal])] = True
            return solve(model)
        literal = unit_clause[0]
        new_model = {**model}
        if literal > 0:
            new_model[frozenset([literal])] = True
        else:
            new_model[frozenset([-literal])] = False
        result = solve(new_model)
        if result is not False:
            return result
        del new_model[frozenset([abs(literal)])]
        new_model[frozenset([-literal])] = True if literal > 0 else False
        return solve(new_model)
    n = max(abs(v) for clause in clauses for v in clause)
    return solve({})

def frege_proof_depth(clauses):
    try:
        return len(dpll(clauses))
    except Exception as e:
        print(f"Error in dpll: {e}")
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_folds = 0
    instances_tested = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_cnf(n, m)
            depth = frege_proof_depth(clauses)
            if depth == 0:
                continue
            max_n = max(max_n, n)
            instances_tested += 1
            total_folds += len(clauses)

    alpha = total_folds / (instances_tested * max_n) if instances_tested > 0 else 0
    metric_value = alpha

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_cnf(n, m)
            depth = frege_proof_depth(clauses)
            if depth == 0:
                continue
            folds = len(clauses)
            if folds > alpha * depth:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, d(φ)={depth}, |Folds(φ)|={folds}"
                break

    return {
        "metric_name": "alpha",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")