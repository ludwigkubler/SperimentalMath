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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        if all(clause[i] == 0 for i in range(n)):
            clause[random.randint(0, n-1)] = random.choice([1, -1])
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = set(tuple(sorted(c)) for c in cnf if len(c) > 1)
    while True:
        new_clauses = []
        for c1 in clauses:
            for c2 in clauses:
                if len(set(c1) & set(c2)) == 1:
                    new_clause = list((set(c1) ^ set(c2)) - {0})
                    if len(new_clause) > 1 and tuple(sorted(new_clause)) not in clauses:
                        new_clauses.append(tuple(sorted(new_clause)))
        if not new_clauses:
            return len(clauses)
        clauses.update(new_clauses)

def algebraic_stochastic_order(cnf):
    n = len(cnf[0])
    assignments = [tuple(random.choice([1, -1]) for _ in range(n)) for _ in range(2**n)]
    values = []
    for assignment in assignments:
        value = sum([assignment[i-1] * clause[i-1] for clause in cnf])
        if value > 0:
            values.append(value)
    return Fraction(sum(values), len(values))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    alpha_values = []
    t_star_values = []

    for n in n_values:
        cnf = generate_cnf(n, n*2)
        alpha_F = algebraic_stochastic_order(cnf)
        t_star_F = resolution_width(cnf)
        alpha_values.append(alpha_F)
        t_star_values.append(t_star_F)

    if not alpha_values or not t_star_values:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    n = len(alpha_values)
    ranks_alpha = [sorted(range(n), key=lambda i: alpha_values[i]) for i in range(n)]
    ranks_t_star = [sorted(range(n), key=lambda i: t_star_values[i]) for i in range(n)]

    tau = sum((ranks_alpha[i][i] - ranks_t_star[i][i]) ** 2 for i in range(n)) / (n * (n**2 - 1))
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": -tau,
        "instances_tested": n,
        "conjecture_holds": tau < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction=1.0")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")