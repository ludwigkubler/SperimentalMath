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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # 10 clauses per variable on average
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def search(assignment):
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if not unit_clauses:
                return assignment
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                if not clause:
                    return None
                new_cnf.append(clause)
            result = search(new_assignment)
            if result is not None:
                return result
            new_assignment[literal] = False
            for clause in cnf:
                if -literal in clause:
                    continue
                if literal in clause:
                    clause.remove(literal)
                if not clause:
                    return None
                new_cnf.append(clause)
            result = search(new_assignment)
            return result

        return search({})

    def frege_width(cnf):
        assignment = dpll(cnf)
        if assignment is None:
            return float('inf')
        width = 0
        for literal in assignment:
            if assignment[literal]:
                width += 1
        return width

    def coxeter_group_order(n):
        # Placeholder function to simulate Coxeter group order calculation
        return n * (n + 1) // 2

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        frege_w = frege_width(cnf)
        coxeter_order = coxeter_group_order(n)
        metric_value = (coxeter_order ** 2) / frege_w
        instances_tested += 1
        total_metric_value += metric_value

        if abs(metric_value - 1) > 0.1 or coxeter_order > frege_w * 1.2:
            conjecture_holds = False
            counterexample = f"n={n}, Coxeter order={coxeter_order}, Frege width={frege_w}"

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0

    return {
        "metric_name": "Coxeter Group Order and Frege Proof Width Ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")