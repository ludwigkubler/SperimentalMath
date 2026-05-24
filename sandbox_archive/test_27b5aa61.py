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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
            clause = random.choice(literals)
            for l in literals:
                if l != clause:
                    clause += ' or ' + str(l)
            clauses.append('(' + clause + ')')
        return ' and '.join(clauses)

    def is_satisfiable(formula):
        # Simplified satisfiability check (not exhaustive)
        for i in range(1, 2**n):
            assignment = {j: ((i >> j) & 1) * 2 - 1 for j in range(n)}
            if all(eval(clause.replace('or', ' or ').replace('and', ' and '), assignment) for clause in formula.split(' and ')):
                return True
        return False

    def compute_symmetry_index(formula):
        n = len(formula.split())
        symmetries = set()
        for i in range(1, 2**n):
            if is_satisfiable(formula):
                symmetries.add(i)
        return len(symmetries)

    def monotone_circuit_complexity(formula):
        # Simplified complexity check (not exhaustive)
        return len(formula.split())

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    symmetry_index = compute_symmetry_index(formula)
    circuit_complexity = monotone_circuit_complexity(formula)

    conjecture_holds = abs(symmetry_index - (1.5 ** n)) < 1e-6
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Symmetry Index: {symmetry_index}, Circuit Complexity: {circuit_complexity}"

    return {
        "metric_name": "Symmetry Index vs Circuit Complexity",
        "metric_value": symmetry_index,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")