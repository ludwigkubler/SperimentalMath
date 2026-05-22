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
        for i in range(1, n+1):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        # Simplified DPLL solver to estimate width
        stack = [(cnf, set())]
        max_width = 0
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                continue
            unit_clauses = [c for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment.copy()
                new_assignment.add(literal)
                stack.append(([(l for l in c if l != literal and -l not in new_assignment) for c in cnf], new_assignment))
                stack.append(([(l for l in c if l != -literal and l not in new_assignment) for c in cnf], new_assignment))
            else:
                literals = [c[0] for c in cnf]
                literal = random.choice(literals)
                new_assignment = assignment.copy()
                new_assignment.add(literal)
                stack.append(([(l for l in c if l != literal and -l not in new_assignment) for c in cnf], new_assignment))
        return max_width
    
    def group_presentation(cnf):
        # Simplified Todd-Coxeter algorithm to find minimal generators
        generators = set()
        relations = []
        for clause in cnf:
            if len(clause) == 2 and abs(clause[0]) != abs(clause[1]):
                generators.add(abs(clause[0]))
                relations.append((abs(clause[0]), abs(clause[1])))
        return generators, relations
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    generators, _ = group_presentation(cnf)
    width = dpll_width(cnf)
    
    return {
        "metric_name": "DPLL Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= math.log(len(generators), 2),
        "counterexample": f"n={n}, width={width}" if not width >= math.log(len(generators), 2) else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_width = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_width} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, width=0\" first_failing_seed={first_failing_seed}")