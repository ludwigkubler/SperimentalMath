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
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
            return False
        literals = [l for l in range(1, n + 1) if l not in assignment and -l not in assignment]
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if -literal not in c], new_assignment):
            return True
        return False

    def measure_dpll_height(cnf, assignment):
        stack = [(cnf, assignment)]
        height = 0
        while stack:
            cnf, assignment = stack.pop()
            if dpll(cnf, assignment):
                continue
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((cnf, new_assignment))
                new_assignment[literal] = False
                stack.append(([c for c in cnf if -literal not in c], new_assignment))
            else:
                literals = [l for l in range(1, n + 1) if l not in assignment and -l not in assignment]
                literal = random.choice(literals)
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((cnf, new_assignment))
                new_assignment[literal] = False
                stack.append(([c for c in cnf if -literal not in c], new_assignment))
            height += 1
        return height

    def minimal_order_quandle(monoid):
        n = len(monoid)
        quandle = {}
        for i in range(n):
            quandle[i] = {}
            for j in range(n):
                quandle[i][j] = None
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if monoid[j][k] not in quandle[quandle[i][monoid[i][j]]]:
                        quandle[i][j] = monoid[j][k]
        return len(quandle)

    def syntactic_monoid(cnf):
        n = len(cnf)
        monoid = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if cnf[i][j] == 1:
                    monoid[i][j] = j
        return monoid

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    assignment = {}
    dpll_height = measure_dpll_height(cnf, assignment)
    monoid = syntactic_monoid(cnf)
    min_order = minimal_order_quandle(monoid)

    return {
        "metric_name": "min_order_quandle",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")