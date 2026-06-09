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

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = [random.choice(variables) * (1 if random.random() < 0.5 else -1)]
        while len(clause) < 3:
            var = random.choice(variables)
            if var not in clause:
                clause.append(var * (1 if random.random() < 0.5 else -1))
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        var = abs(unit_clause[0])
        if unit_clause[0] > 0 and var in assignment or unit_clause[0] < 0 and -var not in assignment:
            return False
        assignment[var] = unit_clause[0] > 0
        return dpll([c for c in cnf if var not in c], assignment)
    pure_literal = next((v for v in variables if all(v not in c or (v < 0 and -v in c) for c in cnf)), None)
    if pure_literal:
        if pure_literal > 0 and pure_literal not in assignment or pure_literal < 0 and -pure_literal not in assignment:
            return False
        assignment[pure_literal] = pure_literal > 0
        return dpll([c for c in cnf if pure_literal not in c], assignment)
    var = random.choice(variables)
    if var not in assignment:
        assignment[var] = True
        if dpll(cnf, assignment):
            return True
        assignment.pop(var)
        assignment[-var] = True
        if dpll(cnf, assignment):
            return True
        assignment.pop(-var)
    return False

def depth(cnf, assignment):
    def helper(clause):
        if not clause:
            return 0
        var = abs(clause[0])
        if var in assignment and (assignment[var] == (clause[0] > 0)):
            return max(helper([lit for lit in clause if lit != var]), helper([lit for lit in clause if lit != -var])) + 1
        return max(helper([lit for lit in clause if lit != var]), helper([lit for lit in clause if lit != -var]))
    return max(helper(clause) for clause in cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice(range(5, 41))
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    assignment = {}
    d = depth(cnf, assignment)
    e_squared_log_n = (d / (n * math.log(n)))**0.5
    return {
        "metric_name": "depth",
        "metric_value": d,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": d <= e_squared_log_n**2 * math.log(n),
        "counterexample": "" if d <= e_squared_log_n**2 * math.log(n) else f"depth({d}) > {e_squared_log_n**2 * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")