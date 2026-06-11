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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment and assignment[literal] != 0:
                return False
            assignment[-literal] = 1
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if dpll(new_cnf, assignment):
                return True
            del assignment[-literal]
        else:
            literal = next((i for i in range(1, n + 1) if i not in assignment), None)
            assignment[literal] = 1
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if dpll(new_cnf, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = 1
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if dpll(new_cnf, assignment):
                return True
            del assignment[-literal]
        return False
    
    def construct_quandle(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        quandle_operation = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
        for i in range(1, 2 * n + 1):
            quandle_operation[i][i] = 1
        for clause in cnf:
            if all(abs(lit) <= n for lit in clause):
                assignment = {}
                if dpll(cnf, assignment):
                    for lit in assignment:
                        if lit < 0 and -lit not in assignment:
                            quandle_operation[i][i] = 1
                        elif lit > 0 and lit not in assignment:
                            quandle_operation[i][i] = 1
        return quandle_operation
    
    def minimal_order(quandle):
        n = len(quandle) // 2
        order = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if quandle[i][j] != 0:
                    order[j] += 1
        return sum(order) / n
    
    def dpll_search_tree_width(cnf):
        assignment = {}
        stack = []
        width = 0
        while True:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0 and literal in assignment and assignment[literal] != 0:
                    return width
                assignment[-literal] = 1
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                stack.append((new_cnf, width))
            else:
                literal = next((i for i in range(1, n + 1) if i not in assignment), None)
                assignment[literal] = 1
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                stack.append((new_cnf, width))
            if len(stack) > width:
                width = len(stack)
            if not stack:
                return width
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        order = minimal_order(construct_quandle(cnf))
        width = dpll_search_tree_width(cnf)
        if not math.isnan(order) and not math.isnan(width):
            instances_tested += 1
            total_order += order
            total_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "DPLL Search Tree Width vs Minimal Order",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip(range(5, 41), range(5, 41))) - 
                               sum(range(5, 41)) * sum(range(5, 41))) / math.sqrt(
        instances_tested * sum((order - mean_order) ** 2 for order in range(5, 41)) * 
        instances_tested * sum((width - mean_width) ** 2 for width in range(5, 41)))
    
    return {
        "metric_name": "DPLL Search Tree Width vs Minimal Order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5 and abs(mean_width - mean_order) <= 10 * mean_order,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")