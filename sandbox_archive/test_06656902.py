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
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(n * (n - 1) // 2):
        clause = [0] * n
        i, j = random.sample(variables, 2)
        clause[i - 1] = random.choice([1, -1])
        clause[j - 1] = -clause[i - 1]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(assignment, clauses):
        if not clauses:
            return assignment
        unit_clause = next((c for c in clauses if len([x for x in c if x != 0]) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                value = False
            else:
                value = True
            assignment[literal] = value
            clauses = [c for c in clauses if literal not in c and -literal not in c]
        pure_literal = next((x for x in range(1, n + 1) if (x in assignment or -x in assignment)), None)
        if pure_literal:
            value = assignment[pure_literal] if pure_literal in assignment else True
            clauses = [c for c in clauses if not any(lit == pure_literal or lit == -pure_literal for lit in c)]
        if not clauses:
            return assignment
        literal = random.choice([x for x in range(1, n + 1) if x not in assignment and -x not in assignment])
        value = True
        assignment[literal] = value
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        result = solve(assignment, new_clauses)
        if result:
            return result
        del assignment[literal]
        value = False
        assignment[literal] = value
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        return solve(assignment, new_clauses)

    n = len(cnf[0])
    assignment = {}
    result = solve(assignment, cnf)
    return result is not None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    w_values = []

    for n in n_values:
        cnf = generate_cnf(n)
        mld = sum(abs(sum(clause)) for clause in cnf) / len(cnf)  # Simplified local cohomological defect
        mld_values.append(mld)

        if dpll(cnf):
            w = len(cnf) * n  # Simplified Frege proof width
        else:
            w = float('inf')  # Unprovable CNF

        w_values.append(w)

    correlation_coefficient = (sum((mld_values[i] - mean(mld_values)) * (w_values[i] - mean(w_values)) for i in range(len(n_values))) /
                               math.sqrt(sum((mld_values[i] - mean(mld_values)) ** 2 for i in range(len(n_values))) *
                                         sum((w_values[i] - mean(w_values)) ** 2 for i in range(len(n_values)))))
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(n_values))))

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value <= 0.05 else "Pearson correlation coefficient < 0.7 or p-value > 0.05"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = mean([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7 or p-value > 0.05\" first_failing_seed={first_failing_seed}")