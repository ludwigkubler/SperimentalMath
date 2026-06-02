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

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.randint(-1, -n), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def tseitin_encoding(cnf):
    literals = set()
    for clause in cnf:
        literals.update(abs(lit) for lit in clause)
    
    new_vars = {lit: i + len(literals) for i, lit in enumerate(literals)}
    tseitin_formula = []
    
    for i, clause in enumerate(cnf):
        var_i = new_vars[i]
        tseitin_formula.append([var_i])
        for literal in clause:
            if literal < 0:
                tseitin_formula.append([-new_vars[abs(literal)], -var_i])
            else:
                tseitin_formula.append([new_vars[literal], -var_i])
    
    return tseitin_formula

def resolution_width(cnf):
    cnf = tseitin_encoding(cnf)
    queue = []
    seen = set()
    
    for clause in cnf:
        if len(clause) == 1:
            literal = clause[0]
            if -literal in seen:
                return float('inf')
            seen.add(literal)
            queue.append((literal, 1))
    
    while queue:
        literal, level = queue.pop(0)
        for clause in cnf:
            if literal in clause:
                new_clause = [x for x in clause if x != literal]
                if -new_clause[0] in seen:
                    return float('inf')
                seen.add(-new_clause[0])
                queue.append((-new_clause[0], level + 1))
    
    return max(level for _, level in queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    tseitin = tseitin_encoding(cnf)
    
    try:
        width = resolution_width(tseitin)
        num_maximal_ideals = len([x for x in range(1, n+1) if -x in tseitin or x in tseitin])
        
        return {
            "metric_name": "#M(φ)",
            "metric_value": num_maximal_ideals,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": num_maximal_ideals <= width,
            "counterexample": "" if num_maximal_ideals <= width else f"num_maximal_ideals={num_maximal_ideals} > width={width}"
        }
    except Exception as e:
        return {
            "metric_name": "#M(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")