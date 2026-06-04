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
    
    def generate_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses, assignment={}):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause if lit not in assignment or assignment[lit] == False)
        
        if not literals:
            return 0
        
        literal = literals.pop()
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        width_pos = 1 + dpll_width(clauses, new_assignment)
        
        new_assignment[literal] = False
        width_neg = 1 + dpll_width(clauses, new_assignment)
        
        return max(width_pos, width_neg)
    
    def symmetric_group_order(n):
        if n == 0:
            return 1
        order = 1
        for i in range(2, n + 1):
            order *= i
        return order
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = dpll_width(formula)
    order = symmetric_group_order(n)
    
    return {
        "metric_name": "DPLL Proof Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width == order,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL width does not match group order\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")