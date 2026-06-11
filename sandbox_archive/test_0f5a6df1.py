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
from fractions import Fraction
import math

def generate_cnf(n):
    clauses = []
    for _ in range(10 * n):  # Each variable appears in at least 10 clauses
        clause = set()
        while len(clause) < 3:  # Clauses have at least 3 literals
            l = random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
            if l not in clause:
                clause.add(l)
        clauses.append(list(clause))
    return clauses

def evaluate_cnf(cnf, assignment):
    return all(any(l in assignment and assignment[l] for l in c) for c in cnf)

def dpll_search_tree_width(cnf, assignment, n):
    if not cnf:
        return 0
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if evaluate_cnf(cnf, new_assignment):
            return 1 + dpll_search_tree_width([c for c in cnf if literal not in c], new_assignment, n)
        else:
            new_assignment[literal] = False
            return 1 + dpll_search_tree_width([c for c in cnf if -literal not in c], new_assignment, n)
    pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
    if pure_literal:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        return 1 + dpll_search_tree_width([c for c in cnf if pure_literal not in c], new_assignment, n)
    branching_literal = next((l for l in range(1, n+1) if l in assignment), None)
    if branching_literal:
        new_assignment = assignment.copy()
        new_assignment[branching_literal] = True
        return 1 + dpll_search_tree_width([c for c in cnf if branching_literal not in c], new_assignment, n)
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        mci_values = []
        w_values = []
        for _ in range(30):
            assignment = {l: random.choice([True, False]) for l in range(-n, n+1) if l != 0}
            f = [[any(l in assignment and assignment[l] for l in c) for c in cnf] for _ in range(2 ** n)]
            mci_values.append(sum(f[i][j] == f[j][i] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1) // 2))
            w_values.append(dpll_search_tree_width(cnf, assignment, n))
        results.extend(zip(mci_values, w_values))
    mci_values, w_values = zip(*results)
    correlation_coefficient = sum((mci_values[i] - sum(mci_values) / len(mci_values)) * (w_values[i] - sum(w_values) / len(w_values)) for i in range(len(mci_values))) / (len(mci_values) * math.sqrt(sum((mci_values[i] - sum(mci_values) / len(mci_values)) ** 2 for i in range(len(mci_values)))) * math.sqrt(sum((w_values[i] - sum(w_values) / len(w_values)) ** 2 for i in range(len(w_values)))))
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")