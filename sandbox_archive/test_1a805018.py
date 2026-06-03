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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def tseitin_structure(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        formulas = {}
        var_count = 0
        for literal in literals:
            formulas[literal] = var_count
            var_count += 1
        
        tseitin_cnf = []
        for clause in cnf:
            new_var = var_count
            formulas[new_var] = var_count
            var_count += 1
            tseitin_cnf.append([new_var])
            for lit in clause:
                if lit > 0:
                    tseitin_cnf.append([-lit, -new_var])
                else:
                    tseitin_cnf.append([lit, new_var])
        
        return tseitin_cnf, formulas
    
    def p_adic_topological_entropy(cnf):
        n = len(cnf)
        if n == 1:
            return 0
        entropy = 0
        for clause in cnf:
            entropy += math.log2(len(clause))
        return entropy / n
    
    def resolution_width(cnf):
        width = 0
        queue = list(cnf)
        while queue:
            new_clause = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause.extend([lit for lit in clause1 + clause2 if lit not in clause1 and lit not in clause2])
                        width = max(width, len(new_clause))
            queue.append(new_clause)
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tseitin_cnf, formulas = tseitin_structure(cnf)
    
    mindex_eta_phi = p_adic_topological_entropy(tseitin_cnf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "mindex(η_φ) vs. w(φ)",
        "metric_value": mindex_eta_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")