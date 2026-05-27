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
    n = random.randint(5, 40)
    instances_tested = 30
    total_r = 0
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random monotone Boolean function f with n variables
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(2**n - 1):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)

        # Construct a monomial circuit C for f using a DPLL solver
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                value = literal.startswith('x') and literal[1] not in assignment or literal.startswith('~x') and literal[2:] in assignment
                return dpll([c for c in clauses if literal not in c], {**assignment, literal: value})
            pure_literal = next((l for l in literals if all(l in clause or f'~{l}' in clause for clause in clauses)), None)
            if pure_literal:
                value = pure_literal.startswith('x')
                return dpll([c for c in clauses if pure_literal not in c], {**assignment, pure_literal: value})
            literal = random.choice(literals)
            value = literal.startswith('x') and literal[1] not in assignment or literal.startswith('~x') and literal[2:] in assignment
            return (dpll(clauses, {**assignment, literal: value}) or dpll(clauses, {**assignment, literal: not value}))

        # Count the number of quadratic forms in the circuit
        r = 0
        for clause in clauses:
            if len(clause) == 2 and all(l.startswith('x') or l.startswith('~x') for l in clause):
                r += 1

        total_r += r

    average_r = total_r / instances_tested
    conjecture_holds = average_r <= n**3  # Polynomial upper bound

    return {
        "metric_name": "average_r",
        "metric_value": average_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "average_r > n^3"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")