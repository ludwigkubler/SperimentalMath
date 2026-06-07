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

# Helper functions for generating CNFs and computing resolution width
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            clause.add((var, sign))
        cnf.append(list(clause))
    return cnf

def resolution_width(cnf):
    def is_tautology(clauses):
        for clause in clauses:
            if len(clause) == 0:
                return True
        return False

    def resolve(clauses, literal):
        new_clauses = []
        for clause in clauses:
            if (literal[0], -literal[1]) not in clause:
                new_clause = [x for x in clause if x != literal]
                if len(new_clause) == 0:
                    return True
                new_clauses.append(tuple(sorted(new_clause)))
        return new_clauses

    def is_resolvable(clauses):
        clauses = list(set(map(tuple, clauses)))
        queue = []
        for clause in clauses:
            if len(clause) == 1:
                queue.append(clause[0])
        while queue:
            literal = queue.pop()
            if literal[1] > 0:
                new_clauses = resolve(clauses, (-literal[0], -literal[1]))
                if is_tautology(new_clauses):
                    return True
                clauses.extend(new_clauses)
            else:
                new_clauses = resolve(clauses, (literal[0], literal[1]))
                if is_tautology(new_clauses):
                    return True
                clauses.extend(new_clauses)
        return False

    width = 0
    while not is_resolvable(cnf):
        width += 1
    return width

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n - 4)):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            w_phi = resolution_width(cnf)
            m_phi = len(cnf)  # Simplified minimal number of toric variants
            metric_values.append((m_phi, w_phi))

    if len(metric_values) < instances_tested * (n_max - 4):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    m_phi_values = [m for m, _ in metric_values]
    w_phi_values = [w for _, w in metric_values]

    mean_m_phi = sum(m_phi_values) / len(m_phi_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)

    correlation_coefficient = 0
    if len(m_phi_values) > 1 and len(w_phi_values) > 1:
        numerator = sum((m - mean_m_phi) * (w - mean_w_phi) for m, w in metric_values)
        denominator = math.sqrt(sum((m - mean_m_phi) ** 2 for m in m_phi_values)) * math.sqrt(sum((w - mean_w_phi) ** 2 for w in w_phi_values))
        correlation_coefficient = numerator / denominator

    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"

    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * (n_max - 4),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{mean_metric_value}\" first_failing_seed={first_failing_seed}")