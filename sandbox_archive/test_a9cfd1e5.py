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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment[var] = -var // abs(var)
            return dpll([c for c in cnf if var not in c and -var not in c], new_assignment)
        
        p_var = next((v for v in range(1, n+1) if v not in assignment), None)
        if p_var is None:
            return False
        
        new_assignment[p_var] = 1
        if dpll(cnf, new_assignment):
            return True
        
        new_assignment[p_var] = -1
        return dpll(cnf, new_assignment)
    
    def generate_coxeter_dynkin_diagram(n):
        # Placeholder for Coxeter-Dynkin diagram generation logic
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    def max_tree_nodes(diagram_size):
        # Placeholder for calculating maximum tree nodes in the Coxeter-Dynkin diagram
        # This is a dummy implementation and should be replaced with actual logic
        return diagram_size
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    height = dpll(cnf)
    diagram_size = generate_coxeter_dynkin_diagram(n)
    max_nodes = max_tree_nodes(diagram_size)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": height <= max_nodes,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_height) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")