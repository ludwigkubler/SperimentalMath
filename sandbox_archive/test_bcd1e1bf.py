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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(literals):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if solve(literals + [literal]):
                return True
            else:
                return solve(literals + [-literal])
        pure_literal = next((l for l in literals if all(l not in c or -l in c for c in cnf)), None)
        if pure_literal is not None:
            new_cnf = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
            return solve(literals + [pure_literal])
        literal = literals[0] if literals else random.choice([1, -1])
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return solve(literals + [literal]) or solve(literals + [-literal])
    return solve([])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = len(dpll(cnf))
    unitary_group_order = n * (n - 1) // 2
    metric_value = math.sqrt(proof_length ** 2)
    instances_tested = 1
    n_max = n
    conjecture_holds = abs(unitary_group_order - proof_length) < 0.1 * proof_length
    counterexample = "" if conjecture_holds else f"Unitary group order {unitary_group_order}, DPLL proof length {proof_length}"
    return {
        "metric_name": "O(φ)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")