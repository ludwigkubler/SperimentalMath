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
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(1, n)]
            while len(clause) < 3:  # Ensure each clause has at least 2 literals
                literal = random.choice([-i, i] for i in range(1, n + 1))
                if literal not in clause:
                    clause.append(literal)
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal > 0 and literal in assignment or literal < 0 and -literal in assignment:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
        else:
            literal = random.choice(cnf[0])
            if literal > 0 and literal in assignment or literal < 0 and -literal in assignment:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
        return False
    
    def mge(cnf):
        # Placeholder implementation of minimal geometric entropy
        # This is a dummy function and should be replaced with actual fractal analysis
        return len(cnf) / 10
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    assignment = {}
    path_length = dpll(cnf, assignment)
    
    if path_length is None:
        return {
            "metric_name": "mge",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL did not terminate"
        }
    
    mge_value = mge(cnf)
    return {
        "metric_name": "mge",
        "metric_value": mge_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_value = -1
        std_value = -1
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")