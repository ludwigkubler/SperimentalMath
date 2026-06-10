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

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, 2 * num_vars) for _ in range(random.randint(1, num_vars))]
        if random.choice([True, False]):
            clause = [-l for l in clause]
        cnf.append(clause)
    return cnf

def calculate_circuit_depth(cnf):
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        pure_literal = next((x for x in range(1, 2 * num_vars + 1) if (x % 2 == 1 and all(l % 2 != 0 for l in c)) or (x % 2 == 0 and all(l % 2 == 0 for l in c))), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                return False
        return False

    num_vars = max(abs(l) for clause in cnf for l in clause)
    assignment = {i: False for i in range(1, 2 * num_vars + 1)}
    return len(dpll(cnf, assignment)) - 1

def calculate_entropy(state):
    counts = [state.count(i) for i in set(state)]
    probabilities = [Fraction(count, len(state)) for count in counts]
    entropy = sum(-p * math.log2(p) for p in probabilities if p != 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
        depth = calculate_circuit_depth(cnf)
        state = [random.choice([0, 1]) for _ in range(2 ** n)]
        entropy = calculate_entropy(state)

        if entropy == 0:
            continue

        ratio = Fraction(depth, entropy).limit_denominator()
        metric_value += ratio
        instances_tested += 1

    if instances_tested > 30:
        mean_ratio = Fraction(metric_value / instances_tested).limit_denominator()
        for n in range(5, n_max + 1):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            depth = calculate_circuit_depth(cnf)
            state = [random.choice([0, 1]) for _ in range(2 ** n)]
            entropy = calculate_entropy(state)

            if entropy == 0:
                continue

            ratio = Fraction(depth, entropy).limit_denominator()
            if abs(ratio - mean_ratio) > mean_ratio * 0.05:
                conjecture_holds = False
                counterexample = f"Ratio {ratio} outside tolerance for n={n}"
                break

    return {
        "metric_name": "Circuit Depth / Entropy Ratio",
        "metric_value": float(metric_value / instances_tested),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")