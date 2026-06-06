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

def dpll(cnf, assignment):
    if not cnf:
        return True
    p, polarity = random.choice(cnf)
    new_assignment = assignment.copy()
    new_assignment[p] = polarity
    if dpll([lit for lit in cnf if not (polarity == lit[1] and p == abs(lit[0]))], new_assignment):
        return True
    new_assignment[p] = -polarity
    return dpll([lit for lit in cnf if not (polarity == -lit[1] and p == abs(lit[0]))], new_assignment)

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = [random.choice([var, -var]) for var in random.sample(variables, random.randint(1, n))]
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 30
    instances_tested = 0
    h_values = []
    w_values = []

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            assignment = {var: None for var in range(1, n + 1)}
            steps = 0

            def hensel_lifting(cnf):
                nonlocal steps
                if not cnf:
                    return True
                p, polarity = random.choice(cnf)
                new_assignment = assignment.copy()
                new_assignment[p] = polarity
                if dpll([lit for lit in cnf if not (polarity == lit[1] and p == abs(lit[0]))], new_assignment):
                    steps += 1
                    return True
                new_assignment[p] = -polarity
                if dpll([lit for lit in cnf if not (polarity == -lit[1] and p == abs(lit[0]))], new_assignment):
                    steps += 1
                    return True
                return False

            if hensel_lifting(cnf):
                h_values.append(steps)
                w_values.append(len(cnf))
                instances_tested += 1

    if not h_values or not w_values:
        return {
            "metric_name": "Hensel Lifting Steps vs DPLL Proof Length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }

    correlation_coefficient = sum((h - h_avg) * (w - w_avg) for h, w in zip(h_values, w_values)) / \
                              (len(h_values) * (sum((h - h_avg) ** 2 for h in h_values) ** 0.5) *
                               (sum((w - w_avg) ** 2 for w in w_values) ** 0.5))
    h_avg = sum(h_values) / len(h_values)
    w_avg = sum(w_values) / len(w_values)

    return {
        "metric_name": "Hensel Lifting Steps vs DPLL Proof Length",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Mapping undefined"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"

    print(result)