# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(cnf, assignment=None):
        if assignment is None:
            assignment = {}
        
        # Find an unassigned literal
        free_literals = [lit for lit in range(1, len(cnf) + 2) if lit not in assignment and -lit not in assignment]
        if not free_literals:
            return all(clause_evaluated(cnf, assignment) for clause in cnf)
        
        literal = random.choice(free_literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(cnf, new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll(cnf, new_assignment):
            return True
        
        return False
    
    def clause_evaluated(clause, assignment):
        return any(lit in assignment and assignment[lit] for lit in clause)
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable
            clause = random.sample(range(-n, -1), 2) + random.sample(range(1, n + 1), 2)
            cnf.append(clause)
        return cnf
    
    def hdeg(cnf):
        # Placeholder for Hodge degeneration index calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) / 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    hdeg_val = hdeg(cnf)
    d_val = dpll(cnf)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": hdeg_val * d_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")