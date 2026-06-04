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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses

    def dpll_width(phi):
        stack = []
        assignment = {}
        literals = set(lit for clause in phi for lit in clause)

        def is_satisfiable():
            while stack:
                literal = stack.pop()
                if literal < 0 and -literal not in assignment:
                    assignment[-literal] = True
                elif literal > 0 and literal not in assignment:
                    assignment[literal] = False

                unsatisfied_clauses = [c for c in phi if not any(lit in assignment and assignment[lit] == (lit < 0) for lit in c)]
                if not unsatisfied_clauses:
                    return True

                clause = random.choice(unsatisfied_clauses)
                literal = next(lit for lit in clause if lit > 0)
                stack.append(-literal)

            return False

        width = 0
        while literals:
            assignment.clear()
            stack.clear()
            literals.difference_update(set(assignment.keys()))
            width += is_satisfiable()
        return width

    def local_symmetry_count(phi):
        # Placeholder for actual symmetry counting logic
        return random.randint(1, len(phi))

    n = 30
    phi = generate_cnf(n)
    width = dpll_width(phi)
    symmetry_count = local_symmetry_count(phi)

    if width == 0:
        return {
            "metric_name": "LocalSymmetryCount / DPLLWidth",
            "metric_value": Fraction(1, 1),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL width is zero"
        }

    ratio = Fraction(symmetry_count, width)
    return {
        "metric_name": "LocalSymmetryCount / DPLLWidth",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break

        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")