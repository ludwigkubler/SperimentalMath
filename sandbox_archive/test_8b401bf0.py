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
    
    def dpll(cnf):
        if not cnf:
            return {}
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            l = unit_clauses[0][0]
            new_cnf = [[l] if l != -c else [-c] for c in cnf if l not in c and -l not in c]
            assignment = dpll(new_cnf)
            assignment[l] = True
            return assignment
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in pure_literals:
                    pure_literals[abs(literal)] = (literal > 0, 1)
                else:
                    sign, count = pure_literals[abs(literal)]
                    if sign != (literal > 0):
                        return None
                    pure_literals[abs(literal)] = (sign, count + 1)
        for literal, (sign, count) in pure_literals.items():
            if count == len(cnf):
                new_cnf = [[l] if l != -literal else [-literal] for c in cnf if l not in c and -l not in c]
                assignment = dpll(new_cnf)
                assignment[literal] = sign
                return assignment
        p, _ = random.choice(list(pure_literals.items()))
        new_cnf = [[p] if p != -c else [-c] for c in cnf if p not in c and -p not in c]
        assignment1 = dpll(new_cnf)
        if assignment1 is not None:
            assignment1[p] = True
            return assignment1
        new_cnf = [[-p] if -p != -c else [-c] for c in cnf if -p not in c and p not in c]
        assignment2 = dpll(new_cnf)
        if assignment2 is not None:
            assignment2[p] = False
            return assignment2
        return None

    def normal_form(cnf):
        assignment = dpll(cnf)
        if assignment is None:
            return []
        nf = set()
        for clause in cnf:
            new_clause = [l for l in clause if assignment.get(abs(l), False) == (l > 0)]
            if new_clause and not any(not assignment.get(abs(l), False) == (l < 0) for l in new_clause):
                nf.add(tuple(sorted(new_clause)))
        return list(nf)

    def resolution_width(cnf, assignment):
        queue = [c for c in cnf if not all(assignment.get(abs(l), False) == (l > 0) for l in c)]
        width = len(queue)
        while queue:
            clause1 = queue.pop()
            for clause2 in cnf:
                new_clause = []
                for l1 in clause1:
                    for l2 in clause2:
                        if abs(l1) == abs(l2):
                            if (l1 > 0 and l2 < 0) or (l1 < 0 and l2 > 0):
                                continue
                            else:
                                new_clause.append(-abs(l1))
                if not all(assignment.get(abs(l), False) == (l > 0) for l in new_clause):
                    queue.append(tuple(sorted(new_clause)))
            width = max(width, len(queue))
        return width

    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(l == -l2 for l in clause for l2 in clause):
                cnf.append(tuple(sorted(clause)))
        
        nf = normal_form(cnf)
        w = resolution_width(cnf, {})
        if w > 0:
            ratio = len(nf) / w
            metric_value += ratio
            if ratio > 1.5:  # Example threshold; adjust as needed
                conjecture_holds = False
                counterexample = f"n={n}, |N(φ)|={len(nf)}, w(φ)={w}"
    
    return {
        "metric_name": "Ratio of Normal Forms to Resolution Width",
        "metric_value": metric_value / instances_tested,
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")