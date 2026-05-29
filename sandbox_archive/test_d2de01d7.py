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

def generate_3cnf(n):
    clauses = []
    for _ in range(10 * n):  # Generate enough clauses to cover all variables
        clause = [random.randint(1, n) if i == 0 else -random.randint(1, n)
                  for i in range(3)]
        random.shuffle(clause)
        clauses.append(tuple(clause))
    return clauses

def truth_table(n, clauses):
    table = {}
    for assignment in product([-1, 1], repeat=n):
        table[assignment] = all(any(lit * x >= 0 for lit in clause) for clause in clauses)
    return table

def hilbert_cube_diameter(table):
    points = list(table.keys())
    n = len(points[0])
    max_dist = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = sum(abs(points[i][k] - points[j][k]) for k in range(n))
            if dist > max_dist:
                max_dist = dist
    return max_dist

def frege_proof_depth(clauses):
    # Simplified DPLL-based solver to estimate proof depth
    def dpll(assignment, clauses):
        unsatisfied_clauses = [c for c in clauses if not any(lit * assignment[abs(lit) - 1] >= 0 for lit in c)]
        if not unsatisfied_clauses:
            return 0
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal // abs(literal)
            return 1 + dpll(new_assignment, [c for c in unsatisfied_clauses if literal not in c])
        pure_literal = next((l for l in range(1, len(assignment) + 1) if (l in assignment and -l not in assignment) or (-l in assignment and l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment[:]
            new_assignment[pure_literal - 1] = 1
            return 1 + dpll(new_assignment, [c for c in unsatisfied_clauses if pure_literal not in c])
        return math.inf

    return dpll([0] * len(clauses), clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    table = truth_table(n, clauses)
    diameter = hilbert_cube_diameter(table)
    depth = frege_proof_depth(clauses)
    metric_value = diameter / depth if depth > 0 else float('inf')
    conjecture_holds = metric_value < 10 * n  # Arbitrary constant c
    counterexample = "" if conjecture_holds else f"n={n}, d={diameter}, depth={depth}"
    return {
        "metric_name": "Diameter/Depth Ratio",
        "metric_value": metric_value,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    from itertools import product

    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")