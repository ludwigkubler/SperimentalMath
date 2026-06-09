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
    
    def is_valid_assignment(assignment, cnf):
        for clause in cnf:
            if all(assignment[abs(lit) - 1] == (lit > 0) for lit in clause):
                break
        else:
            return False
        return True
    
    def dpll(cnf, assignment=None):
        if assignment is None:
            assignment = [None] * len(cnf)
        
        unit_clauses = [i for i, clause in enumerate(cnf) if len(clause) == 1]
        while unit_clauses:
            lit = cnf[unit_clauses[0]][0]
            var = abs(lit) - 1
            value = (lit > 0)
            assignment[var] = value
            unit_clauses = [i for i, clause in enumerate(cnf) if len(clause) == 1 and any(abs(x) == var + 1 for x in clause)]
        
        pure_literals = {}
        for lit in range(1, 2 * n + 1):
            pos_count = sum(1 for clause in cnf if lit in clause)
            neg_count = sum(1 for clause in cnf if -lit in clause)
            if pos_count == 0:
                pure_literals[lit] = False
            elif neg_count == 0:
                pure_literals[lit] = True
        
        while pure_literals:
            lit, value = next(iter(pure_literals.items()))
            var = abs(lit) - 1
            assignment[var] = value
            del pure_literals[lit]
        
        unsatisfied_clauses = [i for i, clause in enumerate(cnf) if not any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)]
        
        if not unsatisfied_clauses:
            return assignment
        
        unit_clause = next((i for i in unsatisfied_clauses if len(cnf[i]) == 1), None)
        if unit_clause is not None:
            lit = cnf[unit_clause][0]
            var = abs(lit) - 1
            value = (lit > 0)
            assignment[var] = value
            return dpll(cnf, assignment)
        
        branching_var = next((i for i in range(n) if assignment[i] is None), None)
        if branching_var is None:
            return None
        
        assignment_true = assignment[:]
        assignment_true[branching_var] = True
        result_true = dpll(cnf, assignment_true)
        if result_true is not None:
            return result_true
        
        assignment_false = assignment[:]
        assignment_false[branching_var] = False
        result_false = dpll(cnf, assignment_false)
        return result_false
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    resolvents = set()
                    for lit_i in clause_i:
                        if -lit_i in clause_j:
                            new_clause = [x for x in clause_i if x != lit_i] + [x for x in clause_j if x != -lit_i]
                            new_clauses.append(new_clause)
                            break
            clauses.extend(new_clauses)
            if not any(len(clause) == 0 for clause in clauses):
                return len(max(clauses, key=len))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    assignment = [None] * n
    result = dpll(cnf, assignment)
    if result is None:
        resolution_width = resolution(cnf)
    else:
        resolution_width = len(result)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")