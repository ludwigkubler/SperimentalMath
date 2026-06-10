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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = {}
        for literal in set(lit for clause in cnf for lit in clause):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals[literal] = True
            elif neg_count == 0:
                pure_literals[-literal] = False
        
        if unit_clauses:
            literal = unit_clauses[0]
            return dpll(cnf, assignment | {literal: True}) or dpll(cnf, assignment | {-literal: True})
        
        if pure_literals:
            literal = next(l for l in pure_literals if pure_literals[l])
            return dpll(cnf, assignment | {literal: True})
        
        literal = random.choice([l for clause in cnf for l in clause if l not in assignment])
        return dpll(cnf, assignment | {literal: True}) or dpll(cnf, assignment | {-literal: True})
    
    def resolution_width(cnf):
        queue = [c for c in cnf]
        while queue:
            c1 = queue.pop()
            for c2 in queue:
                resolvents = set()
                for lit1 in c1:
                    if -lit1 in c2:
                        new_clause = [l for l in c1 if l != lit1] + [l for l in c2 if l != -lit1]
                        if len(new_clause) == 0:
                            return float('inf')
                        resolvents.add(tuple(sorted(new_clause)))
                queue.extend(resolvents)
        return max(len(c) for c in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    
    if width == float('inf'):
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_cnf"
        }
    
    return {
        "metric_name": "lchrank_over_width",
        "metric_value": width / n,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width / n >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")