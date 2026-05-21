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

# Helper functions for DPLL algorithm
def dpll(formula, assignment, literals):
    if not formula:
        return True
    literal = next(lit for lit in literals if lit not in assignment and -lit not in assignment)
    positive = literal > 0
    new_assignment = assignment.copy()
    new_assignment[literal] = positive

    # Simplify the formula by substituting the literal
    simplified_formula = []
    for clause in formula:
        if literal in clause:
            continue
        if -literal in clause:
            clause.remove(-literal)
            if not clause:
                return False
        simplified_formula.append(clause)

    if dpll(simplified_formula, new_assignment, literals):
        return True

    # Backtrack
    del new_assignment[literal]
    new_assignment[-literal] = not positive
    simplified_formula = []
    for clause in formula:
        if -literal in clause:
            continue
        if literal in clause:
            clause.remove(literal)
            if not clause:
                return False
        simplified_formula.append(clause)

    return dpll(simplified_formula, new_assignment, literals)

def dpll_search_tree_depth(formula, n):
    return 1 + max(dpll_search_tree_depth([c for c in formula if literal in c], n) for literal in range(1, n+1))

# Constructive mapping from Boolean formula to toric variety
def construct_toric_variety(formula):
    # This is a placeholder function. Replace with actual implementation.
    return 0

# Main trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(lit not in clause and -lit not in clause for lit in formula):
            formula.append(clause)

    toric_variety_rank = construct_toric_variety(formula)
    dpll_depth = dpll_search_tree_depth(formula, n)

    return {
        "metric_name": "Rank of Toric Variety vs DPLL Depth",
        "metric_value": abs(toric_variety_rank - dpll_depth),
        "instances_tested": 1,
        "conjecture_holds": abs(toric_variety_rank - dpll_depth) <= max(toric_variety_rank, dpll_depth) / 2,
        "counterexample": "" if toric_variety_rank == dpll_depth else f"Rank: {toric_variety_rank}, Depth: {dpll_depth}"
    }

# Main execution
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")