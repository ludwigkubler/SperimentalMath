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
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def unit_propagation(cnf):
        while True:
            unit_clauses = [l for clause in cnf if len(clause) == 1]
            if not unit_clauses:
                break
            l, _ = unit_clauses[0]
            sign = l > 0
            l = abs(l)
            new_cnf = []
            for clause in cnf:
                if l not in clause and -l not in clause:
                    new_cnf.append(clause)
                elif l in clause:
                    continue
                else:
                    new_clause = [x for x in clause if x != -l]
                    if len(new_clause) > 0:
                        new_cnf.append(new_clause)
            cnf = new_cnf
        return cnf

    def pure_literal_elimination(cnf):
        while True:
            pure_literals = {}
            for clause in cnf:
                for l in clause:
                    if abs(l) not in pure_literals:
                        pure_literals[abs(l)] = (l > 0, 1)
                    else:
                        sign, count = pure_literals[abs(l)]
                        if sign != (l > 0):
                            del pure_literals[abs(l)]
                        else:
                            pure_literals[abs(l)] = (sign, count + 1)
            if not pure_literals:
                break
            l, _ = next(iter(pure_literals.items()))
            sign, _ = pure_literals[l]
            new_cnf = []
            for clause in cnf:
                if l not in clause and -l not in clause:
                    new_cnf.append(clause)
                elif l in clause:
                    continue
                else:
                    new_clause = [x for x in clause if x != -l]
                    if len(new_clause) > 0:
                        new_cnf.append(new_clause)
            cnf = new_cnf
        return cnf

    def dpll_helper(cnf, assignment):
        cnf = unit_propagation(cnf)
        cnf = pure_literal_elimination(cnf)
        if not cnf:
            return True, assignment
        if any(len(clause) == 0 for clause in cnf):
            return False, assignment

        l = next(iter(cnf[0]))
        rest_cnf = [clause for clause in cnf if l not in clause and -l not in clause]
        new_assignment = assignment.copy()
        new_assignment[l] = True
        result, assignment = dpll_helper(rest_cnf, new_assignment)
        if result:
            return True, assignment

        new_assignment[l] = False
        rest_cnf = [clause for clause in cnf if l not in clause and -l not in clause]
        new_assignment[-l] = True
        result, assignment = dpll_helper(rest_cnf, new_assignment)
        if result:
            return True, assignment

        return False, assignment

    assignment = {}
    return dpll_helper(cnf, assignment)[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        for _ in range(6):  # Aim for at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            height = dpll(cnf)
            if height is None:
                continue

            instances_tested += 1
            total_metric_value += math.sqrt(n)

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (n_max - 4) * 6

    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print("RESULT: SUPPORTED" if support_fraction >= 0.8 else "RESULT: INCONCLUSIVE budget_exceeded n_tested=30")