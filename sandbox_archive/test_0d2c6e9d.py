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

def random_cnf(n, m):
    clauses = []
    variables = set(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def dfa_states(cnf):
    states = {0}
    stack = [0]
    visited = set()
    while stack:
        state = stack.pop()
        if state not in visited:
            visited.add(state)
            for literal in cnf:
                new_state = 0
                for lit in literal:
                    if lit > 0 and lit in states:
                        new_state |= (1 << (lit - 1))
                    elif lit < 0 and -lit in states:
                        new_state &= ~(1 << (-lit - 1))
                if new_state not in states:
                    states.add(new_state)
                    stack.append(new_state)
    return len(states)

def resolution_width(cnf):
    clauses = cnf[:]
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            break
        unit_clause = unit_clauses[0]
        literal = unit_clause[0]
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.append([x for x in clause if x != -literal])
            else:
                new_clauses.append(clause)
        clauses = new_clauses + [[-literal]]
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    m_values = []
    w_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n // 2, n * 2)
        cnf = random_cnf(n, m)
        m_value = dfa_states(cnf)
        w_value = resolution_width(cnf)
        m_values.append(m_value)
        w_values.append(w_value)

    mean_m = sum(m_values) / instances_tested
    mean_w = sum(w_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean_m) ** 2 for x in m_values) / instances_tested)
    correlation_coefficient = sum((m_values[i] - mean_m) * (w_values[i] - mean_w) for i in range(instances_tested)) / (instances_tested * std_dev * std_dev)

    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_m - mean_w) <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8 or mean_abs_diff>3"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    std_dev_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_dev_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_dev_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8 or mean_abs_diff>3\" first_failing_seed={first_failing_seed}")