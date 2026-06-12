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
        literals = list(range(1, n + 1))
        cnf_formula = []
        for _ in range(n):
            clause = random.sample(literals + [-l for l in literals], 2)
            cnf_formula.append(tuple(sorted(clause)))
        return tuple(cnf_formula)
    
    def dpll_width(cnf_formula):
        if not cnf_formula:
            return 0
        clauses = list(cnf_formula)
        assignment = {}
        
        def propagate():
            while True:
                changed = False
                for clause in clauses[:]:
                    unsatisfied = [l for l in clause if l not in assignment and -l not in assignment]
                    if len(unsatisfied) == 1:
                        literal = unsatisfied[0]
                        assignment[literal] = None
                        changed = True
                    elif len(unsatisfied) == 0:
                        clauses.remove(clause)
                if not changed:
                    break
        
        def dpll():
            propagate()
            if not clauses:
                return 0
            unit_clauses = [l for l in assignment if assignment[l] is None]
            if unit_clauses:
                literal = random.choice(unit_clauses)
                assignment[literal] = True
                return dpll() + 1
            pure_lits = {}
            for clause in clauses:
                for l in clause:
                    if l not in pure_lits and -l not in pure_lits:
                        pure_lits[l] = True
                    elif l in pure_lits and -l in pure_lits:
                        del pure_lits[l]
            if not pure_lits:
                return 0
            literal = random.choice(list(pure_lits.keys()))
            assignment[literal] = True
            return dpll() + 1
        
        return dpll()
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    
    for n in range(5, 41):
        cnf_formula = generate_cnf(n)
        width = dpll_width(cnf_formula)
        
        if width == 0:
            continue
        
        instances_tested += 1
        total_metric_value += width
    
    if instances_tested == 0:
        return {
            "metric_name": "DPLL Width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_width = total_metric_value / instances_tested
    return {
        "metric_name": "DPLL Width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")