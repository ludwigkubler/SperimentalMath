# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def generate_3cnf(n, alpha):
        clauses = []
        for _ in range(int(alpha * n * (n - 1) / 2)):
            clause = [random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)]
            while len(set(clause)) != 3:
                clause = [random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)]
            clauses.append(clause)
        return clauses

    def evaluate_formula(formula, assignment):
        for clause in formula:
            if not any(assignment[var] == (var < 0) for var in clause):
                return False
        return True

    def dpll(formula, assignment, unit_clause=None):
        if len(formula) == 0:
            return True
        if unit_clause is not None:
            assignment[unit_clause[0]] = unit_clause[1]
            formula = [c for c in formula if unit_clause[0] not in c and -unit_clause[0] not in c]
        var, polarity = next((v, p) for v in range(len(assignment)) for p in (True, False) if assignment[v] is None)
        assignment[var] = polarity
        if dpll(formula, assignment):
            return True
        assignment[var] = not polarity
        formula = [c for c in formula if var not in c and -var not in c]
        if dpll(formula, assignment):
            return True
        return False

    def phi_f(z, n, clauses):
        a_k = [0] * (n + 1)
        for assignment in range(2**n):
            weight = bin(assignment).count('1')
            if evaluate_formula(clauses, [bool((assignment >> i) & 1) for i in range(n)]):
                a_k[weight] += 1
        return sum(a_k[k] * z**k for k in range(n + 1))

    def newton_inequality_defect(n, clauses):
        a_k = [0] * (n + 1)
        for assignment in range(2**n):
            weight = bin(assignment).count('1')
            if evaluate_formula(clauses, [bool((assignment >> i) & 1) for i in range(n)]):
                a_k[weight] += 1
        delta = max(max(0, (a_k[k-1] * a_k[k+1]) / (a_k[k]**2) - ((k-1)*(n-k+1)) / (k*(n-k+1))) for k in range(1, n))
        return delta

    def leaf_count(n, clauses):
        assignment = [None] * n
        stack = [(clauses, assignment)]
        leaves = 0
        while stack:
            formula, assignment = stack.pop()
            if len(formula) == 0:
                leaves += 1
                continue
            var, polarity = next((v, p) for v in range(n) for p in (True, False) if assignment[v] is None)
            assignment[var] = polarity
            new_formula = [c for c in formula if var not in c and -var not in c]
            stack.append((new_formula, assignment[:]))
            assignment[var] = not polarity
        return leaves

    n_values = [14, 16, 18, 20]
    alpha_values = [3.6, 3.8, 4.0]
    instances_tested = 0
    total_slack = 0
    num_supported = 0

    for n in n_values:
        for alpha in alpha_values:
            for _ in range(30):
                clauses = generate_3cnf(n, alpha)
                delta = newton_inequality_defect(n, clauses)
                leaves = leaf_count(n, clauses)
                slack = math.log2(leaves) - 0.25 * n * math.log2(1 + delta) + 4 * math.sqrt(n)
                total_slack += slack
                instances_tested += 1

                if slack >= 0:
                    num_supported += 1

    mean_slack = total_slack / instances_tested
    support_fraction = num_supported / instances_tested

    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.80,
        "counterexample": "" if support_fraction >= 0.80 else "support_fraction < 0.80"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.80:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.80\" first_failing_seed={first_failing_seed}")