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

def generate_k_sat_instance(n, k):
    instance = []
    for _ in range(k):
        clause = set()
        while len(clause) < 3:
            lit = random.randint(-n, n)
            if abs(lit) not in clause:
                clause.add(lit)
        instance.append(list(clause))
    return instance

def is_satisfiable(instance):
    def backtrack(assignment=None):
        assignment = assignment or {}
        if len(assignment) == num_vars:
            return True
        var = next((v for v in range(1, num_vars + 1) if v not in assignment), None)
        if var is None:
            return False
        for value in [True, False]:
            assignment[var] = value
            if all(any(assignment[abs(lit)] == lit for lit in clause) for clause in instance):
                if backtrack(assignment):
                    return True
            del assignment[var]
        return False

    num_vars = max(abs(lit) for clause in instance for lit in clause)
    return backtrack()

def compute_hypergeometric_function_rank(circuit):
    # Placeholder function to compute the hypergeometric function rank of a circuit
    # This is a dummy implementation and should be replaced with actual logic
    return len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    num_trials = 30
    instances_tested = 0
    satisfiable_ranks = []
    unsatisfiable_ranks = []
    n_max = 5

    for _ in range(num_trials):
        n = random.choice([5, 10, 15, 20, 30, 40])
        k = min(3, n)
        instance = generate_k_sat_instance(n, k)
        satisfiable = is_satisfiable(instance)

        if satisfiable:
            circuit_ranks = [compute_hypergeometric_function_rank(circuit) for _ in range(10)]
            satisfiable_ranks.extend(circuit_ranks)
        else:
            unsatisfiable_ranks.append(compute_hypergeometric_function_rank(instance))

        instances_tested += 1
        n_max = max(n_max, n)

    if not satisfiable_ranks or not unsatisfiable_ranks:
        return {
            "metric_name": "Hypergeometric Function Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    satisfiable_avg = sum(satisfiable_ranks) / len(satisfiable_ranks)
    unsatisfiable_avg = min(unsatisfiable_ranks)

    correlation_coefficient = (len(satisfiable_ranks) * sum(x*y for x, y in zip(satisfiable_ranks, range(len(satisfiable_ranks)))) -
                               len(satisfiable_ranks) * satisfiable_avg * (len(satisfiable_ranks) - 1) / 2) / \
                              math.sqrt((len(satisfiable_ranks) * sum(x*x for x in satisfiable_ranks) - len(satisfiable_ranks) * satisfiable_avg**2) *
                                        (len(satisfiable_ranks) * sum(y*y for y in range(len(satisfiable_ranks))) - len(satisfiable_ranks)**2))

    conjecture_holds = correlation_coefficient >= 0.9 and unsatisfiable_avg >= 2 * len(unsatisfiable_ranks)
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "Hypergeometric Function Rank",
        "metric_value": satisfiable_avg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    satisfiable_avg = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
    unsatisfiable_avg = min(result["metric_value"] for result in results if not result["conjecture_holds"])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={satisfiable_avg} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")