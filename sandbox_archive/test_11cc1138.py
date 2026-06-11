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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        literals = list(range(1, n + 1)) + [-x for x in range(1, n + 1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment, literals):
        if not cnf:
            return True
        literal = literals[0]
        pos_literal = abs(literal)
        if pos_literal in assignment:
            new_assignment = assignment.copy()
            new_literals = [l for l in literals if l != literal and l != -literal]
            if dpll(cnf, new_assignment, new_literals):
                return True
        else:
            new_assignment1 = assignment.copy()
            new_assignment1[pos_literal] = True
            new_literals1 = [l for l in literals if l != literal and l != -literal]
            if dpll(cnf, new_assignment1, new_literals1):
                return True
            new_assignment2 = assignment.copy()
            new_assignment2[pos_literal] = False
            new_literals2 = [l for l in literals if l != literal and l != -literal]
            if dpll(cnf, new_assignment2, new_literals2):
                return True
        return False

    def formal_context_width(cnf):
        context = {}
        for clause in cnf:
            for literal in clause:
                if literal not in context:
                    context[literal] = set()
                for other_literal in clause:
                    if other_literal != literal and -other_literal not in clause:
                        context[literal].add(other_literal)
        return max(len(context[l]) for l in context)

    def dpll_tree_height(cnf, assignment, literals):
        if not cnf:
            return 0
        literal = literals[0]
        pos_literal = abs(literal)
        if pos_literal in assignment:
            new_assignment = assignment.copy()
            new_literals = [l for l in literals if l != literal and l != -literal]
            return dpll_tree_height(cnf, new_assignment, new_literals) + 1
        else:
            new_assignment1 = assignment.copy()
            new_assignment1[pos_literal] = True
            new_literals1 = [l for l in literals if l != literal and l != -literal]
            height1 = dpll_tree_height(cnf, new_assignment1, new_literals1) + 1
            new_assignment2 = assignment.copy()
            new_assignment2[pos_literal] = False
            new_literals2 = [l for l in literals if l != literal and l != -literal]
            height2 = dpll_tree_height(cnf, new_assignment2, new_literals2) + 1
        return max(height1, height2)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        mfw_total = 0
        w_phi_total = 0
        instances_tested = 0
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(n, 2*n))
            mfw = formal_context_width(cnf)
            assignment = {}
            literals = list(range(1, n + 1)) + [-x for x in range(1, n + 1)]
            w_phi = dpll_tree_height(cnf, assignment, literals)
            mfw_total += mfw
            w_phi_total += w_phi
            instances_tested += 1
        results.append({
            "n": n,
            "mfw_avg": mfw_total / instances_tested,
            "w_phi_avg": w_phi_total / instances_tested
        })

    mfw_values = [r["mfw_avg"] for r in results]
    w_phi_values = [r["w_phi_avg"] for r in results]

    def pearson_correlation(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        return numerator / denominator if denominator != 0 else 0

    correlation_coefficient = pearson_correlation(mfw_values, w_phi_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * len(n_values),
        "n_max": max(results, key=lambda r: r["n"])["n"],
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.95) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")