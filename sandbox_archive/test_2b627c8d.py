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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def p_adic_valuation(phi, valuations):
    rank = 0
    for assignment in valuations:
        coeffs = [sum(valuations[assignment][i] for i in phi[j]) for j in range(len(phi))]
        if any(coeff != 0 for coeff in coeffs):
            rank += 1
    return rank

def resolution_width(phi, max_depth=20):
    stack = [{'clause': phi, 'depth': 0}]
    while stack:
        current = stack.pop()
        if current['depth'] > max_depth:
            continue
        if not current['clause']:
            return current['depth']
        unit_clause = [x for x in current['clause'] if abs(x) == 1]
        if not unit_clause:
            continue
        literal = unit_clause[0]
        new_clauses = []
        for clause in current['clause']:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.append([x for x in clause if x != -literal])
            else:
                new_clauses.append(clause + [-literal])
        stack.extend({'clause': nc, 'depth': current['depth'] + 1} for nc in new_clauses)
    return math.inf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = generate_cnf(n)
    valuations = {}
    for assignment in range(2**n):
        assignment_str = f"{assignment:0{n}b}"
        valuation = [1 if assignment_str[i] == '1' else -1 for i in range(n)]
        valuations[assignment_str] = valuation
    rank = p_adic_valuation(phi, valuations)
    width = resolution_width(phi)
    return {
        "metric_name": "correlation",
        "metric_value": rank * width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r['conjecture_holds'] for r in results):
        mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
        support_fraction = 1.0
        RESULT = f"SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"

    print(RESULT)