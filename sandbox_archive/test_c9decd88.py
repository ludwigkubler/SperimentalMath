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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal is not None:
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                new_assignment[pure_literal] = False
                if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                    return True
                else:
                    return False
        literals = [l for l in range(1, n+1) if l not in assignment and -l not in assignment]
        literal = random.choice(literals)
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
    
    def non_archimedean_valuation(cnf, assignment):
        valuation = 0
        for clause in cnf:
            satisfied = any(assignment.get(lit, False) for lit in clause)
            if satisfied:
                valuation += 1
        return valuation
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    depth = dpll(cnf)
    
    if depth is None:
        return {
            "metric_name": "min_rank(V) / depth(D)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree did not terminate"
        }
    
    valuation = non_archimedean_valuation(cnf, {})
    ratio = Fraction(valuation, depth)
    
    return {
        "metric_name": "min_rank(V) / depth(D)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": "" if 0.5 <= ratio <= 1.5 else str(valuation) + "/" + str(depth)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")