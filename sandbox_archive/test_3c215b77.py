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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(2**m - 1):
            clause = [random.randint(-m, m-1) for _ in range(random.randint(1, m))]
            cnf.append(clause)
        return cnf
    
    def tseitin_encoding(cnf):
        literals = set()
        new_vars = {}
        clauses = []
        
        def encode_clause(clause):
            nonlocal literals, new_vars
            if len(clause) == 1:
                literals.add(abs(clause[0]))
                return clause[0]
            else:
                new_var = max(literals) + 1
                literals.add(new_var)
                new_vars[new_var] = clause
                clauses.append([new_var, -encode_clause(clause[:len(clause)//2])])
                clauses.append([new_var, -encode_clause(clause[len(clause)//2:])])
                return new_var
        
        for clause in cnf:
            encode_clause(clause)
        
        for var, clause in new_vars.items():
            clauses.extend([-var] + [-l for l in clause if l > 0])
        
        return clauses
    
    def solve(lits_true, cls):
        stack = []
        model = {}
        
        def dpll(cls, model):
            if not cls:
                return True
            unit_clause = next((c for c in cls if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                if lit < 0 and -lit in model:
                    return False
                model[abs(lit)] = lit > 0
                cls = [c for c in cls if not any(l in c for l in (lit, -lit))]
            pure_literal = next((l for l in literals if all(l not in c or -l in c for c in cls)), None)
            if pure_literal is not None:
                model[abs(pure_literal)] = pure_literal > 0
                cls = [c for c in cls if not any(l in c for l in (pure_literal, -pure_literal))]
            if not cls:
                return True
            lit = next(iter(cls))
            stack.append((lit, model.copy()))
            while stack:
                lit, model = stack.pop()
                if lit < 0 and -lit in model:
                    continue
                model[abs(lit)] = lit > 0
                cls = [c for c in cls if not any(l in c for l in (lit, -lit))]
                if dpll(cls, model):
                    return True
                del model[abs(lit)]
                stack.append((-lit, model.copy()))
            return False
        
        return solve(lits_true, cls)
    
    def min_order(cnf):
        m = len(cnf[0])
        tensor = [[0] * (2**m) for _ in range(2**m)]
        
        def assign_tensor(var, value):
            nonlocal tensor
            if var > 0:
                row = var - 1
                col = sum([2**(i-1) for i in range(1, m+1) if abs(value) & (1 << (i-1))])
            else:
                row = -var - 1
                col = sum([2**(i-1) for i in range(1, m+1) if value & (1 << (i-1))])
            tensor[row][col] += 1
        
        for clause in cnf:
            for lit in clause:
                assign_tensor(abs(lit), lit)
        
        return max(max(row) for row in tensor)
    
    def proof_length(cnf):
        clauses = tseitin_encoding(cnf)
        lits_true = set()
        cls = [c[:] for c in clauses]
        
        def solve(cls, model):
            if not cls:
                return True
            unit_clause = next((c for c in cls if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                if lit < 0 and -lit in model:
                    return False
                model[abs(lit)] = lit > 0
                cls = [c for c in cls if not any(l in c for l in (lit, -lit))]
            pure_literal = next((l for l in literals if all(l not in c or -l in c for c in cls)), None)
            if pure_literal is not None:
                model[abs(pure_literal)] = pure_literal > 0
                cls = [c for c in cls if not any(l in c for l in (pure_literal, -pure_literal))]
            if not cls:
                return True
            lit = next(iter(cls))
            stack.append((lit, model.copy()))
            while stack:
                lit, model = stack.pop()
                if lit < 0 and -lit in model:
                    continue
                model[abs(lit)] = lit > 0
                cls = [c for c in cls if not any(l in c for l in (lit, -lit))]
                if solve(cls, model):
                    return True
                del model[abs(lit)]
                stack.append((-lit, model.copy()))
            return False
        
        return len(clauses)
    
    m = random.randint(5, 30)
    cnf = generate_cnf(m)
    min_order_value = min_order(cnf)
    proof_length_value = proof_length(cnf)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_value,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": abs(min_order_value - proof_length_value) < 0.5 * max(min_order_value, proof_length_value),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")