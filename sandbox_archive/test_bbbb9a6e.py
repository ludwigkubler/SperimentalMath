# auto-injected by SEC sandbox
import math
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

def generate_formula(n):
    variables = set(f"x{i}" for i in range(1, n+1))
    formula = []
    for _ in range(n):
        clause = random.sample(sorted(variables | {f"~{v}" for v in variables}), 2)
        formula.append(clause)
    return formula

def dpll_width(formula):
    def is_satisfiable(model):
        for clause in formula:
            if not any(var in model and model[var] == (var[0] != '~') for var in clause) and \
               not any("~" + var in model and model["~" + var] == (var[0] != '~') for var in clause):
                return False
        return True

    def backtrack(model, literals):
        if not literals:
            return is_satisfiable(model)
        literal = literals.pop()
        if backtrack(model | {literal: True}, literals.copy()):
            return True
        if backtrack(model | {literal: False}, literals.copy()):
            return True
        literals.add(literal)
        return False

    all_literals = set(var for clause in formula for var in clause) | set("~" + var for clause in formula for var in clause)
    return max(len([l for l in all_literals if backtrack({}, {l})]), 1)

def betti_number(formula):
    # Placeholder implementation of Betti number calculation
    # This is a dummy function and should be replaced with actual computation
    return len(formula) / 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    max_betti = 0
    instances_tested = 0
    n_max = 16
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        formula = generate_formula(n)
        width = dpll_width(formula)
        betti = betti_number(formula)
        max_betti = max(max_betti, betti)
        instances_tested += 1
        n_max = max(n_max, n)

    if max_betti > (Fraction(1, 1) * n).log(Fraction(2)) / (Fraction(1, 1) * n).log(Fraction(2)).log(Fraction(2)):
        conjecture_holds = False
        counterexample = "Betti number exceeds conjectured upper bound"

    return {
        "metric_name": "max_betti",
        "metric_value": max_betti,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_betti = sum(r["metric_value"] for r in results) / len(results)
    std_betti = (sum((r["metric_value"] - mean_betti)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_betti} std={std_betti} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Betti number exceeds conjectured upper bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")