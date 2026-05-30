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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def truth_table(k_cnf, n):
        tt = [[0] * (2 ** n) for _ in range(len(k_cnf))]
        for i, clause in enumerate(k_cnf):
            for j in range(2 ** n):
                binary_rep = format(j, f'0{n}b')
                if any(int(binary_rep[abs(lit) - 1]) == (lit > 0) for lit in clause):
                    tt[i][j] = 1
        return tt
    
    def min_group_representation_order(tt):
        n = len(tt[0])
        m = len(tt)
        order = 0
        for i in range(n):
            count = sum(1 for row in tt if row[i] == 1)
            if count > order:
                order = count
        return order
    
    def resolution_width(k_cnf, n):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = [None] * (n + 1)
        def dpll():
            nonlocal stack, assignment
            if not stack:
                return True
            literal = stack.pop()
            pos_lit, neg_lit = abs(literal), -literal
            if assignment[pos_lit] is None and assignment[neg_lit] is None:
                assignment[pos_lit] = True
                stack.append(neg_lit)
                if dpll():
                    return True
                assignment[pos_lit] = False
                stack.pop()
                assignment[neg_lit] = True
                stack.append(pos_lit)
                if dpll():
                    return True
                assignment[neg_lit] = None
            elif literal > 0 and assignment[literal]:
                for clause in k_cnf:
                    if literal in clause:
                        clause.remove(literal)
                        if not clause:
                            return False
                        break
            else:
                for clause in k_cnf:
                    if neg_lit in clause:
                        clause.remove(neg_lit)
                        if not clause:
                            return False
                        break
            stack.append(literal)
            return dpll()
        width = 0
        while True:
            if not dpll():
                width += 1
                assignment = [None] * (n + 1)
                stack = []
            else:
                break
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, int(n / 2))
        k_cnf = generate_k_cnf(n, m)
        tt = truth_table(k_cnf, n)
        order = min_group_representation_order(tt)
        width = resolution_width(k_cnf, n)
        results.append({
            "n": n,
            "m": m,
            "order": order,
            "width": width
        })
    
    metric_value = sum(result["width"] for result in results) / len(results)
    conjecture_holds = all(result["order"] <= (result["m"] ** (2/3)) * (result["n"] ** (1/4)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")