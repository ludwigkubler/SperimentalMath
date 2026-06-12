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
    
    def tseitin_transformation(clauses):
        new_vars = {}
        tseitin_clauses = []
        var_counter = 1
        
        def get_new_var():
            nonlocal var_counter
            var = f'x{var_counter}'
            var_counter += 1
            return var
        
        for clause in clauses:
            if len(clause) == 1:
                new_var = get_new_var()
                tseitin_clauses.append([new_var, -clause[0]])
                new_vars[clause[0]] = new_var
            else:
                new_var = get_new_var()
                tseitin_clauses.append([-new_var] + clause)
                for literal in clause:
                    if literal not in new_vars:
                        tseitin_clauses.append([new_var, -literal])
                        new_vars[literal] = get_new_var()
        return tseitin_clauses, new_vars
    
    def resolution(clauses):
        clauses = list(clauses)
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            clauses.remove(unit_clause)
            new_clauses = []
            for clause in clauses:
                if -literal in clause:
                    index = clause.index(-literal)
                    new_clause = clause[:index] + clause[index+1:]
                    if len(new_clause) == 0:
                        return None
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(clause)
            clauses.extend(new_clauses)
        return clauses
    
    def quandle_entropy(clauses):
        # Simplified entropy calculation for demonstration purposes
        return len(clauses) / 2
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(1, 3)
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(num_vars)]
        clauses.append(clause)
    
    tseitin_clauses, new_vars = tseitin_transformation(clauses)
    resolution_result = resolution(tseitin_clauses)
    
    if resolution_result is None:
        return {
            "metric_name": "quandle_entropy",
            "metric_value": 0,
            "instances_tested": n,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    quandle_ent = quandle_entropy(tseitin_clauses)
    resolution_width = len(resolution_result)
    
    return {
        "metric_name": "quandle_entropy",
        "metric_value": quandle_ent,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    quandle_ent_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    resolution_widths = [r["instances_tested"] for r in results if r["conjecture_holds"]]
    
    mean_quandle_ent = sum(quandle_ent_values) / len(quandle_ent_values)
    std_quandle_ent = math.sqrt(sum((x - mean_quandle_ent) ** 2 for x in quandle_ent_values) / len(quandle_ent_values))
    support_fraction = len(quandle_ent_values) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={mean_quandle_ent} std={std_quandle_ent} support_fraction={support_fraction}"
    else:
        RESULT = f"FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}"
    
    print(RESULT)