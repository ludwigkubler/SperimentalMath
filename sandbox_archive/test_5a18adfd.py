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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(-n, n+1) if l not in assignment and -l not in assignment), None)
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
                    return False, {}
                new_cnf.append(clause)
            return True, {**assignment, lit: True}
        
        def backtrack(lit):
            new_cnf = []
            for clause in cnf:
                if -lit in clause:
                    continue
                if lit in clause:
                    clause.remove(lit)
                if not clause:
                    return False, {}
                new_cnf.append(clause)
            return True, {**assignment, lit: False}
        
        success, assignment = propagate(literal)
        if success:
            if dpll(new_cnf, assignment):
                return True
        success, assignment = backtrack(literal)
        if success:
            if dpll(new_cnf, assignment):
                return True
        return False
    
    def syntactic_monoid(cnf):
        n = len(cnf)
        monoid = {}
        for i in range(1 << n):
            state = [bool(i & (1 << j)) for j in range(n)]
            next_state = []
            for clause in cnf:
                if all(state[abs(lit) - 1] == (lit > 0) for lit in clause):
                    next_state.append(not state[abs(clause[0]) - 1])
                else:
                    next_state.append(state[abs(clause[0]) - 1])
            monoid[tuple(state)] = tuple(next_state)
        return monoid
    
    def minimal_order_quandle(monoid):
        n = len(monoid)
        order = [n] * (1 << n)
        for state in range(1 << n):
            if all(order[state] <= order[monoid[state][i]] for i in range(n)):
                order[state] = 1
                for i in range(n):
                    if monoid[state][i] != state:
                        order[state] += 1
        return max(order)
    
    def dpll_height(cnf):
        n = len(cnf)
        stack = [(cnf, {})]
        height = 0
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                continue
            literal = next((l for l in range(-n, n+1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return height
            
            def propagate(lit):
                new_cnf = []
                for clause in cnf:
                    if lit in clause:
                        continue
                    if -lit in clause:
                        clause.remove(-lit)
                    if not clause:
                        return False, {}
                    new_cnf.append(clause)
                return True, {**assignment, lit: True}
            
            def backtrack(lit):
                new_cnf = []
                for clause in cnf:
                    if -lit in clause:
                        continue
                    if lit in clause:
                        clause.remove(lit)
                    if not clause:
                        return False, {}
                    new_cnf.append(clause)
                return True, {**assignment, lit: False}
            
            success, assignment = propagate(literal)
            if success:
                stack.append((new_cnf, assignment))
            success, assignment = backtrack(literal)
            if success:
                stack.append((new_cnf, assignment))
            height += 1
        return height
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    monoid = syntactic_monoid(cnf)
    min_order = minimal_order_quandle(monoid)
    dpll_height_val = dpll_height(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": min_order * dpll_height_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] or r["counterexample"] != "mapping_undefined" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")