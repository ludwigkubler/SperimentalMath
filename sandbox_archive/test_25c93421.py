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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment, literals):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = abs(unit_clause[0])
            value = unit_clause[0] > 0
            if literal in assignment and assignment[literal] != value:
                return False
            assignment[literal] = value
            literals.remove(literal)
            cnf = [c for c in cnf if literal not in c]
            return dpll(cnf, assignment, literals)
        pure_literal = next((l for l in literals if all(l in c or -l in c for c in cnf)), None)
        if pure_literal:
            value = True
            if pure_literal < 0:
                value = False
                pure_literal = -pure_literal
            assignment[pure_literal] = value
            literals.remove(pure_literal)
            cnf = [c for c in cnf if pure_literal not in c]
            return dpll(cnf, assignment, literals)
        literal = random.choice(literals)
        value = True
        if literal < 0:
            value = False
            literal = -literal
        assignment[literal] = value
        literals.remove(literal)
        cnf_true = [c for c in cnf if literal not in c]
        cnf_false = [c for c in cnf if -literal not in c]
        return dpll(cnf_true, assignment, literals) or dpll(cnf_false, assignment, literals)
    
    def measure_dpll_height(cnf):
        assignment = {}
        literals = list(range(1, len(cnf) + 1))
        height = 0
        stack = [(cnf, assignment, literals, height)]
        while stack:
            cnf, assignment, literals, height = stack.pop()
            if dpll(cnf, assignment, literals):
                return height
            stack.append((cnf, assignment.copy(), literals.copy(), height + 1))
        return -1
    
    def syntactic_monoid(cnf):
        n = len(cnf)
        monoid = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            monoid[i][i] = i
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                monoid[x][y] = y
                monoid[y][x] = x
            elif clause[0] > 0 and clause[1] < 0:
                monoid[x][-y] = -y
                monoid[-y][x] = -x
            elif clause[0] < 0 and clause[1] > 0:
                monoid[-x][y] = y
                monoid[y][-x] = -x
            else:
                monoid[-x][-y] = -y
                monoid[-y][-x] = -x
        return monoid
    
    def minimal_order_quandle(monoid):
        n = len(monoid)
        for order in range(1, n + 1):
            quandle = [[0] * (n + 1) for _ in range(n + 1)]
            for i in range(1, n + 1):
                quandle[i][i] = i
            for j in range(1, n + 1):
                for k in range(1, n + 1):
                    if monoid[j][k] != 0:
                        quandle[monoid[i][j]][monoid[i][k]] = monoid[i][monoid[j][k]]
            if is_isomorphic(quandle, monoid):
                return order
        return n
    
    def is_isomorphic(q1, q2):
        n = len(q1)
        for perm in permutations(n):
            if all(q1[perm[i]][perm[j]] == q2[i][j] for i in range(1, n + 1) for j in range(1, n + 1)):
                return True
        return False
    
    def permutations(n):
        if n == 0:
            yield ()
        else:
            for perm in permutations(n - 1):
                for i in range(n):
                    yield perm[:i] + (n,) + perm[i:i]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    monoid = syntactic_monoid(cnf)
    min_order = minimal_order_quandle(monoid)
    dpll_height = measure_dpll_height(cnf)
    
    if dpll_height == -1:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_search_tree_height_not_computed"
        }
    
    correlation = (min_order - dpll_height) / math.sqrt(min_order**2 + dpll_height**2)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, min_order_quandle={min(r['metric_value'], key=abs)}, dpll_height={max(r['metric_value'], key=abs)}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break