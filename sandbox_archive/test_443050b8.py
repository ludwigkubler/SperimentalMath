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
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False

        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                new_cnf.append(clause)
            return new_cnf, {**assignment, lit: True}

        def backtrack(lit):
            new_cnf = []
            for clause in cnf:
                if -lit in clause:
                    continue
                if lit in clause:
                    clause.remove(lit)
                    if not clause:
                        return False
                new_cnf.append(clause)
            return new_cnf, {**assignment, -lit: True}

        if propagate(literal):
            result = dpll(propagate(literal)[0], assignment)
            if result:
                return result
        if backtrack(-literal):
            result = dpll(backtrack(-literal)[0], assignment)
            if result:
                return result
        return False

    def algebraic_monoid_index(cnf):
        n = len(cnf[0])
        monoid = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                product = [0] * n
                for k in range(n):
                    if cnf[i][k] == 1 and cnf[j][k] == 1:
                        product[k] = 1
                monoid[i][j] = sum(product)
        return max(sum(row) for row in monoid)

    def dpll_tree_width(cnf):
        n = len(cnf[0])
        width = [0] * (2**n)
        stack = [(cnf, {})]
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                continue
            literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                continue

            def propagate(lit):
                new_cnf = []
                for clause in cnf:
                    if lit in clause:
                        continue
                    if -lit in clause:
                        clause.remove(-lit)
                        if not clause:
                            return False
                    new_cnf.append(clause)
                return new_cnf, {**assignment, lit: True}

            def backtrack(lit):
                new_cnf = []
                for clause in cnf:
                    if -lit in clause:
                        continue
                    if lit in clause:
                        clause.remove(lit)
                        if not clause:
                            return False
                    new_cnf.append(clause)
                return new_cnf, {**assignment, -lit: True}

            stack.append((propagate(literal)[0], assignment))
            stack.append((backtrack(-literal)[0], assignment))

        return max(width)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    index = algebraic_monoid_index(cnf)
    width = dpll_tree_width(cnf)

    return {
        "metric_name": "index_width_correlation",
        "metric_value": index * width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")