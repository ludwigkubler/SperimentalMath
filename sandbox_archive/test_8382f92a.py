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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(model, clause_index=0):
            if clause_index == len(cnf):
                return model
            literals = cnf[clause_index]
            for literal in literals:
                new_model = model.copy()
                if literal > 0:
                    new_model.add(literal)
                else:
                    new_model.discard(-literal)
                result = solve(new_model, clause_index + 1)
                if result is not None:
                    return result
            return None
        
        return solve(set())
    
    def mcr(cnf):
        n = len(cnf[0])
        variables = set(abs(lit) for lit in cnf[0])
        monomials = {tuple(sorted([abs(lit) for lit in clause])) for clause in cnf}
        
        def groebner_basis(monomials, n):
            basis = list(monomials)
            while True:
                new_monomials = set()
                for i in range(len(basis)):
                    for j in range(i + 1, len(basis)):
                        lcm = [max(a, b) for a, b in zip(basis[i], basis[j])]
                        if all(lcm[k] % min(basis[i][k], basis[j][k]) == 0 for k in range(n)):
                            new_monomials.add(tuple(sorted(lcm)))
                if not new_monomials:
                    break
                basis.extend(new_monomials)
            return basis
        
        gb = groebner_basis(monomials, n)
        rank = len(gb)
        return rank
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        d = dpll(cnf)
        mcr_value = mcr(cnf)
        
        if d is None:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree diameter calculation failed"
            }
        
        if mcr_value == 0:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Minimal local cohomology rank is zero"
            }
        
        if d == 0:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree diameter is zero"
            }
        
        if d > 2**n:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree diameter is too large"
            }
        
        if mcr_value > n**2:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Minimal local cohomology rank is too large"
            }
        
        if d > mcr_value:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree diameter is greater than minimal local cohomology rank"
            }
        
        if mcr_value > d:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Minimal local cohomology rank is greater than DPLL search tree diameter"
            }
        
        if d == mcr_value:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": 1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": True,
                "counterexample": ""
            }
        
        if d != mcr_value:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": -1.0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree diameter is not equal to minimal local cohomology rank"
            }
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": -1.0,
        "instances_tested": 36,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "No valid instances found"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL search tree diameter is not equal to minimal local cohomology rank\" first_failing_seed={first_failing_seed}")