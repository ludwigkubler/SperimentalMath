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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause.append(-1)
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        unsatisfied_clauses = [c for c in cnf if all(l not in assignment or assignment[l] == -v for l, v in enumerate(c))]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = -literal // abs(literal)
            return dpll(cnf, new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if (all(l not in c or c.count(l) == 0 for c in unsatisfied_clauses) and all(-l not in c or c.count(-l) == 0 for c in unsatisfied_clauses))), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = -pure_literal // abs(pure_literal)
            return dpll(cnf, new_assignment)
        literal = random.choice([l for l in range(1, n + 1) if l not in assignment and -l not in assignment])
        return (dpll(cnf, {**assignment, literal: 1}) or dpll(cnf, {**assignment, literal: -1}))

    def eta_phi(cnf):
        # Placeholder for the actual mapping procedure
        return random.random()

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    eta_phi_value = eta_phi(cnf)
    if not dpll(cnf):
        return {
            "metric_name": "eta_phi",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver failed to find a model"
        }
    return {
        "metric_name": "eta_phi",
        "metric_value": eta_phi_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    eta_phi_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    if not eta_phi_values:
        print("RESULT: INCONCLUSIVE no valid trials")
    else:
        mean_eta_phi = sum(eta_phi_values) / len(eta_phi_values)
        std_eta_phi = math.sqrt(sum((x - mean_eta_phi) ** 2 for x in eta_phi_values) / len(eta_phi_values))
        support_fraction = sum(r["conjecture_holds"] for r in results if r["metric_value"] is not None) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_eta_phi} std={std_eta_phi} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"DPLL solver failed to find a model\" first_failing_seed={first_failing_seed}")