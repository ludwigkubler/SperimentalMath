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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            cnf.append(clause)
        return cnf
    
    def construct_quandle(cnf):
        quandle = {}
        for lit in range(1, max(abs(lit) for clause in cnf for lit in clause) + 1):
            quandle[lit] = set()
            quandle[-lit] = set()
        for clause in cnf:
            pos_lit = abs(clause[0])
            neg_lit = abs(clause[1])
            quandle[pos_lit].add((True, clause))
            quandle[neg_lit].add((False, clause))
        return quandle
    
    def count_non_trivial_entanglements(quandle):
        entanglements = 0
        for lit in quandle:
            for other_lit in quandle:
                if lit != other_lit and any(clause[1] == other_clause[1] for clause in quandle[lit] for other_clause in quandle[other_lit]):
                    entanglements += 1
        return entanglements
    
    def dpll_search_tree_size(cnf):
        n = len([lit for lit, _ in cnf if lit > 0])
        stack = [(cnf, [])]
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                return len(assignment)
            unit_clause = next((clause for clause in cnf if sum(lit in assignment or -lit in assignment for lit in clause) == 1), None)
            if unit_clause:
                literal = [lit for lit in unit_clause if lit not in assignment and -lit not in assignment][0]
                stack.append(([(l, c) for l, c in cnf if l != literal], assignment + [(literal, True)]))
                stack.append(([(l, c) for l, c in cnf if l != -literal], assignment + [(-literal, False)]))
            else:
                literal = next(lit for lit in range(1, n+1) if lit not in assignment and -lit not in assignment)
                stack.append(([(l, c) for l, c in cnf if l != literal], assignment + [(literal, True)]))
                stack.append(([(l, c) for l, c in cnf if l != -literal], assignment + [(-literal, False)]))
        return float('inf')
    
    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    cnf = generate_cnf(n, m)
    quandle = construct_quandle(cnf)
    entanglements = count_non_trivial_entanglements(quandle)
    dpll_size = dpll_search_tree_size(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": entanglements * dpll_size,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(res["conjecture_holds"] for res in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")