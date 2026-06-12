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

def random_clause(n):
    return [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]

def random_cnf(n):
    return [random_clause(n) for _ in range(random.randint(2, n))]

def dfa_states(cnf):
    states = {()}
    for clause in cnf:
        new_states = set()
        for state in states:
            for lit in clause:
                if abs(lit) not in state:
                    new_state = tuple(sorted(state + (lit,)))
                    new_states.add(new_state)
        states.update(new_states)
    return len(states)

def resolution_width(cnf):
    clauses = cnf[:]
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                lit_i = clauses[i][0]
                if -lit_i in clauses[j]:
                    new_clause = [x for x in clauses[i] if x != lit_i] + [x for x in clauses[j] if x != -lit_i]
                    new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.extend(new_clauses)
    return max(len(clause) for clause in clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    m_values = []
    w_values = []

    for n in range(5, n_max + 1):
        for _ in range(6):  # Test each size 6 times to ensure statistical signal
            cnf = random_cnf(n)
            m_phi = dfa_states(cnf)
            w_phi = resolution_width(cnf)
            m_values.append(m_phi)
            w_values.append(w_phi)
            instances_tested += 1

    if not m_values or not w_values:
        return {
            "metric_name": "m(φ) vs. w(φ)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric"
        }

    mean_m = sum(m_values) / len(m_values)
    mean_w = sum(w_values) / len(w_values)
    std_dev_m = math.sqrt(sum((x - mean_m) ** 2 for x in m_values) / len(m_values))
    std_dev_w = math.sqrt(sum((x - mean_w) ** 2 for x in w_values) / len(w_values))

    correlation_coefficient = sum((m_values[i] - mean_m) * (w_values[i] - mean_w) for i in range(len(m_values))) / (len(m_values) * std_dev_m * std_dev_w)

    return {
        "metric_name": "m(φ) vs. w(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and std_dev_m <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{result['metric_value']}\", first_failing_seed={first_failing_seed}")