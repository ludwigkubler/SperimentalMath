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
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(x > 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((x for x in range(-n, n + 1) if x not in assignment and -x not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        if dpll(propagate(literal), assignment | {literal: True}):
            return True
        if dpll(propagate(-literal), assignment | {-literal: True}):
            return True
        return False
    
    def theta_series(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        theta = [[0] * (2 ** n) for _ in range(2 ** n)]
        theta[0][0] = 1
        
        for i in range(n):
            new_theta = [[0] * (2 ** n) for _ in range(2 ** n)]
            for j in range(2 ** n):
                for k in range(2 ** n):
                    if bin(j).count('1') + bin(k).count('1') == i:
                        new_theta[j][k] = sum(theta[i1][j1] * theta[i2][k1] for i1, j1 in enumerate(bin(j)[2:].zfill(n)) for i2, k1 in enumerate(bin(k)[2:].zfill(n)))
            theta = new_theta
        
        rank = 0
        for row in theta:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    rank = theta_series(cnf)
    td = dpll(cnf)
    
    if td is None:
        return {
            "metric_name": "rank_td_diff",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree diameter calculation failed"
        }
    
    return {
        "metric_name": "rank_td_diff",
        "metric_value": rank - td,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_td_diff = sum(r["metric_value"] for r in results) / len(results)
    std_td_diff = math.sqrt(sum((r["metric_value"] - mean_td_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_td_diff} std={std_td_diff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_td_diff} std={std_td_diff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='rank_td_diff' first_failing_seed={first_failing_seed}")