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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):
            clause = [random.randint(-1, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment, literals):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)-1] = literal > 0
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment, literals)
        pure_literal = next((l for l in literals if (l in assignment or -l in assignment) == False), None)
        if pure_literal is None:
            return False
        new_literals = [l for l in literals if l != pure_literal and l != -pure_literal]
        return dpll(cnf, assignment, new_literals)

    def shannon_entropy(assignment):
        n = len(assignment)
        p_true = sum(1 for a in assignment if a) / n
        p_false = 1 - p_true
        entropy = -p_true * math.log2(p_true) - p_false * math.log2(p_false)
        return entropy

    def dpll_tree_width(cnf):
        literals = set(abs(l) for l in sum(cnf, []))
        width = 0
        for literal in literals:
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            width = max(width, dpll_tree_width(new_cnf))
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            assignment = [None] * n
            width = dpll_tree_width(cnf)
            entropy = shannon_entropy(assignment)
            metric_values.append((n, entropy, width))
            instances_tested += 1
            n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "Entropy vs DPLL Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation_coefficient = 0
    mean_entropy = sum(v[1] for v in metric_values) / len(metric_values)
    mean_width = sum(v[2] for v in metric_values) / len(metric_values)

    for n, entropy, width in metric_values:
        correlation_coefficient += (entropy - mean_entropy) * (width - mean_width)
    correlation_coefficient /= len(metric_values) * math.sqrt(sum((v[1] - mean_entropy)**2 for v in metric_values)) * math.sqrt(sum((v[2] - mean_width)**2 for v in metric_values))

    if correlation_coefficient < 0.9:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"

    return {
        "metric_name": "Entropy vs DPLL Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{results[first_failing_seed]['metric_value']:.2f}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")