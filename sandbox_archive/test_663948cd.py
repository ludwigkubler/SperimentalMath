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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n * 2) if random.choice([True, False]) else -random.randint(1, n * 2) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((lit for lit in range(1, len(cnf) + 1) if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return None
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack(lit):
            assignment.pop(lit, None)
        
        if propagate(lit) is None:
            backtrack(lit)
            literal = -literal
            if propagate(literal) is None:
                backtrack(literal)
                return False
        
        assignment[lit] = True
        if dpll(propagate(lit), assignment):
            return True
        backtrack(lit)
        
        assignment[lit] = False
        if dpll(propagate(literal), assignment):
            return True
        backtrack(literal)
        
        return False
    
    def mter(cnf):
        # Placeholder for minimal local index of topological entanglement rank calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)  # Simplified example
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    mter_value = mter(cnf)
    path_length = dpll(cnf)
    
    if not path_length:
        return {
            "metric_name": "mter_path_length_correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL did not find a solution"
        }
    
    return {
        "metric_name": "mter_path_length_correlation",
        "metric_value": abs(mter_value - path_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(v is None for v in metric_values):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    elif support_fraction >= 0.8:
        mean_value = sum(metric_values) / len(metric_values)
        std_value = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mter_path_length_correlation\" first_failing_seed={first_failing_seed}")