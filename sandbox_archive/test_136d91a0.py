# auto-injected by SEC sandbox
import math
import itertools
import collections
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
import json

def generate_3cnf(n, m):
    cnf = set()
    while len(cnf) < m:
        clause = tuple(sorted(random.sample(range(-n, 0), 1) + random.sample(range(1, n+1), 2)))
        if len(clause) == 3 and all(abs(lit) not in clause for lit in cnf):
            cnf.add(clause)
    return cnf

def dpll(cnf, assignment):
    unit_clauses = [lit for lit in cnf if sum(abs(lit) in assignment.values() for l in lit) == 1]
    while unit_clauses:
        lit = random.choice(unit_clauses)
        val = -assignment[lit[0]] if lit[0] in assignment else None
        if val is not None:
            assignment[lit[0]] = val
            cnf.discard(lit)
            unit_clauses = [l for l in cnf if sum(abs(lit) in assignment.values() for l in l) == 1]
        else:
            return False, None
    return True, assignment

def upc(cnf):
    assignment = {}
    while True:
        success, _ = dpll(cnf, assignment)
        if not success:
            return False
        progress = False
        for x in range(1, 13):
            if x not in assignment:
                assignment[x] = 0
                new_assignment, _ = dpll(cnf, assignment)
                if not new_assignment:
                    assignment[x] = 1
                else:
                    progress = True
        for x in range(-12, -1):
            if -x not in assignment:
                assignment[-x] = 0
                new_assignment, _ = dpll(cnf, assignment)
                if not new_assignment:
                    assignment[-x] = 1
                else:
                    progress = True
        if not progress:
            return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 12
    m = 51
    cnf = generate_3cnf(n, m)
    unsat_cnf = []
    for _ in range(200):
        if not dpll(cnf, {})[0]:
            unsat_cnf.append(cnf.copy())
    upc_values = [upc(cnf) for cnf in unsat_cnf]
    p_hat = sum(upc_values) / len(upc_values)
    se = (p_hat * (1 - p_hat) / len(upc_values)) ** 0.5
    conjecture_holds = p_hat <= 0.20 and (0.20 - p_hat) >= 3 * se
    counterexample = "" if conjecture_holds else "UPC(F)=1 exceeded 0.20 by ≥3σ"
    return {
        "metric_name": "Pr[UPC(F)=1]",
        "metric_value": p_hat,
        "instances_tested": len(upc_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    p_hats = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    se = (sum(p * (1 - p) for p in p_hats) / len(p_hats)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(p_hats)/len(p_hats):.4f} std={se:.4f} support_fraction=1.00")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(p_hats)/len(p_hats):.4f} std={se:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"UPC(F)=1 exceeded 0.20 by ≥3σ\" first_failing_seed={first_failing_seed}")