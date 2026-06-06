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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        literal = random.choice(list(clauses))
        var, polarity = literal[0], literal[1]
        if var in assignment and assignment[var] != polarity:
            return False
        assignment[var] = polarity
        new_clauses = [c for c in clauses if not all(lit in assignment and assignment[lit] == (lit[1] if lit[0] == var else not lit[1]) for lit in c)]
        if dpll(new_clauses, assignment):
            return True
        del assignment[var]
        new_clauses = [c for c in clauses if all(lit in assignment and assignment[lit] != (lit[1] if lit[0] == var else not lit[1]) for lit in c)]
        if dpll(new_clauses, assignment):
            return True
        return False
    
    def resolution_width(cnf):
        assignment = {}
        return len(assignment) if dpll(cnf, assignment) else float('inf')
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(-n, 0), 1) + random.sample(range(1, n+1), random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    m = random.randint(1, 40 - n)
    cnf = generate_cnf(m, n)
    
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": f"CNF: {cnf}, Width: {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif any(r["metric_value"] <= 3 or r["p_value"] >= 0.05 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["metric_value"] <= 3 or r["p_value"] >= 0.05)
        print(f"RESULT: FALSIFIED counterexample='low correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")