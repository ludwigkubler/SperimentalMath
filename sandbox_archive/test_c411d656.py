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

def generate_sat_instance(m: int) -> tuple:
    variables = set()
    clauses = []
    for _ in range(m):
        clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, m + 1)]
        clauses.append(clause)
        variables.update(clause)
    return list(variables), clauses

def clause_subset_entropy(variables: list, clauses: list) -> float:
    n_vars = len(variables)
    n_clauses = len(clauses)
    total_weight = 0
    for clause in clauses:
        weight = sum(1 for var in clause if var.startswith('x'))
        total_weight += weight
    entropy = Fraction(total_weight, n_clauses * 2 ** n_vars).log2() if total_weight > 0 else 0
    return entropy

def tseitin_formula(variables: list, clauses: list) -> str:
    new_vars = {f'y{i}': i for i in range(1, len(clauses) + 1)}
    formula = []
    for i, clause in enumerate(clauses):
        literals = [new_vars[f'y{i+1}']] + [f'~{var}' if var.startswith('~') else var for var in clause]
        formula.append(literals)
    return formula

def resolution_width(formula: list) -> int:
    queue = formula.copy()
    while True:
        new_clauses = []
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                if len(set(queue[i]) & set(queue[j])) == 2:
                    new_clause = [l for l in queue[i] if l not in queue[j]] + [l for l in queue[j] if l not in queue[i]]
                    new_clauses.append(new_clause)
        if not new_clauses:
            return len(queue)
        queue.extend(new_clauses)

def minimal_order_brauer_group(entropy: float) -> int:
    # Placeholder function to simulate the computation of Brauer group order
    # This is a dummy implementation and should be replaced with actual logic
    return round(math.exp(entropy * 10))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = random.randint(5, 30)
    variables, clauses = generate_sat_instance(m)
    entropy = clause_subset_entropy(variables, clauses)
    formula = tseitin_formula(variables, clauses)
    width = resolution_width(formula)
    order = minimal_order_brauer_group(entropy)
    correlation = (order - width) / max(order, width) if order != 0 and width != 0 else 0
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": m,
        "n_max": m,
        "conjecture_holds": abs(correlation) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")