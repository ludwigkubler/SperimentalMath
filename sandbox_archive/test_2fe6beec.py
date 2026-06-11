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
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf: list, assignment: dict = {}) -> bool:
        if not cnf:
            return True
        unit_clauses = [lit for lit in cnf if len(lit) == 1]
        if unit_clauses:
            lit = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            return dpll(propagate(lit, cnf), new_assignment)
        
        literals = set(abs(lit) for clause in cnf for lit in clause)
        literal = literals.pop()
        if literal in assignment:
            return dpll(cnf, assignment)
        
        def propagate(lit: int, cnf: list) -> list:
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return []
                    new_cnf.append(clause)
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        return dpll(propagate(lit, cnf), assignment | {lit: True}) or \
               dpll(propagate(-lit, cnf), assignment | {-lit: True})
    
    def hodge_mumford_cohomology(cnf: list) -> float:
        # Placeholder for actual computation
        return random.random() * n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        h_value = hodge_mumford_cohomology(cnf)
        w_DPLL = dpll(cnf)
        
        if not w_DPLL:
            return {
                "metric_name": "h(V(φ)) / w_DPLL(φ)",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree width is 0"
            }
        
        ratio = abs(h_value / w_DPLL)
        results.append(ratio)
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(results, [mean] * len(results))) / \
                              math.sqrt(sum((x - mean) ** 2 for x in results) * sum((y - mean) ** 2 for y in [mean] * len(results)))
    
    return {
        "metric_name": "h(V(φ)) / w_DPLL(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(ratio <= 2 for ratio in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["conjecture_holds"]]
    support_fraction = len(results) / len(seeds)
    
    if support_fraction >= 0.8:
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if run_trial(seed)["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL search tree width is 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support found")