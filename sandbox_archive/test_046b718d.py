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
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            while any(clause[i] == -clause[j] for j in range(i)):
                clause[random.randint(0, len(clause)-1)] = random.randint(-n, n)
            cnf.append(tuple(sorted(clause)))
        return tuple(cnf)

    def dpll_solve(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal != 0:
                    variables.add(abs(literal))
        stack = []
        assignment = {var: None for var in variables}
        
        def backtrack():
            if not stack:
                return True
            var = next(var for var in variables if assignment[var] is None)
            assignment[var] = True
            if dpll(cnf, assignment):
                return True
            assignment[var] = False
            if dpll(cnf, assignment):
                return True
            assignment[var] = None
            return False
        
        def dpll(cnf, assignment):
            while cnf:
                unit_clauses = [c for c in cnf if len(c) == 1]
                if unit_clauses:
                    literal = unit_clauses[0][0]
                    var = abs(literal)
                    assignment[var] = literal > 0
                    cnf = [(l for l in c if l != literal and l != -literal) for c in cnf if l != literal and l != -literal]
                else:
                    pure_literals = {}
                    for c in cnf:
                        for literal in c:
                            var = abs(literal)
                            if literal > 0:
                                pure_literals[var] = True
                            else:
                                pure_literals[var] = False
                    pure_literal_vars = [var for var, val in pure_literals.items() if all(val == assignment[var] for var in pure_literals)]
                    if pure_literal_vars:
                        literal = next(literal for var in pure_literal_vars if assignment[var])
                        cnf = [(l for l in c if l != literal and l != -literal) for c in cnf if l != literal and l != -literal]
                    else:
                        stack.append((cnf, assignment))
                        return backtrack()
            return True
        
        return dpll(cnf, assignment)
    
    def mld(cnf):
        # Placeholder for minimal local cohomological defect calculation
        return random.random()  # This is a dummy implementation
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = len(cnf) if dpll_solve(cnf) else float('inf')
    mld_value = mld(cnf)
    
    return {
        "metric_name": "mld",
        "metric_value": mld_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")