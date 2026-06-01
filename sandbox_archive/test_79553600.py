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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def tseitin_encoding(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        new_vars = {lit: f'x{lit}' for lit in literals}
        
        formulas = []
        for i, clause in enumerate(cnf):
            var = f'y{i + 1}'
            formulas.append(f'{var} <-> ({" ∨ ".join(new_vars[lit] if lit > 0 else f'¬{new_vars[-lit]}' for lit in clause)})')
        
        return formulas
    
    def dpll_search_tree(cnf):
        stack = []
        assignment = {}
        def solve():
            while True:
                if not cnf:
                    return True
                unit_clause = next((c for c in cnf if len(c) == 1), None)
                if unit_clause:
                    lit = unit_clause[0]
                    if lit > 0 and lit not in assignment:
                        assignment[lit] = True
                    elif lit < 0 and -lit not in assignment:
                        assignment[-lit] = False
                    else:
                        return False
                    cnf = [c for c in cnf if lit not in c and -lit not in c]
                else:
                    literal, polarity = next((l, True) for l in literals if l not in assignment)
                    stack.append((literal, polarity))
                    assignment[literal] = polarity
            return False
        
        def backtrack():
            while stack:
                literal, polarity = stack.pop()
                del assignment[literal]
                cnf.append([literal if polarity else -literal])
                if solve():
                    return True
                del assignment[-literal]
                cnf.remove([-literal if polarity else literal])
            return False
        
        return backtrack() and len(assignment)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tseitin_formulas = tseitin_encoding(cnf)
    td = dpll_search_tree(tseitin_formulas)
    
    if td is None:
        return {
            "metric_name": "DPLL Search Tree Diameter",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_search_tree returned None"
        }
    
    min_local_ring_norm = sum(len(c) for c in cnf)
    log_fact_n = sum(math.log(i + 1) for i in range(n))
    
    return {
        "metric_name": "DPLL Search Tree Diameter",
        "metric_value": td,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_td = sum(result["metric_value"] for result in results) / len(results)
        std_td = math.sqrt(sum((result["metric_value"] - mean_td) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_td} std={std_td} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")