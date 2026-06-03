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
        clauses = []
        for i in range(1 << m):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(m)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def tseitin_encoding(cnf, n):
        literals = list(range(1, n + 1))
        new_vars = [n + i for i in range(len(cnf))]
        cnf_tseitin = []
        
        for i, clause in enumerate(cnf):
            literal = new_vars[i]
            clause_tseitin = [-l for l in literals] + [literal]
            cnf_tseitin.append(clause_tseitin)
            
            for j in range(len(literals)):
                for k in range(j + 1, len(literals)):
                    cnf_tseitin.append([-literals[j], -literals[k], literal])
        
        return cnf_tseitin
    
    def solve(cnf, cls):
        stack = []
        assignment = {}
        unit_clauses = [c for c in cnf if len(c) == 1]
        
        while True:
            while unit_clauses:
                lit = unit_clauses.pop()
                val = lit[0] > 0
                literal = abs(lit[0])
                if literal not in assignment:
                    assignment[literal] = val
                    stack.append((literal, val))
                else:
                    if assignment[literal] != val:
                        return False
            
            unit_clauses = []
            for c in cnf:
                unsatisfied = [l for l in c if abs(l) not in assignment]
                if len(unsatisfied) == 1:
                    lit = unsatisfied[0]
                    val = lit > 0
                    literal = abs(lit)
                    if literal not in assignment:
                        assignment[literal] = val
                        stack.append((literal, val))
                    else:
                        if assignment[literal] != val:
                            return False
            
            if not unit_clauses and not stack:
                return True
        
        return False
    
    def min_order(cnf):
        m = len(cnf[0])
        n = 2 ** (m - 1)
        tensor = [[0 for _ in range(n)] for _ in range(n)]
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    row, col = divmod(lit - 1, n // 2)
                else:
                    row, col = divmod(-lit - 1, n // 2)
                tensor[row][col] += 1
        
        rank = 0
        for i in range(n):
            if any(tensor[i]):
                rank += 1
        
        return rank
    
    def proof_length(cnf):
        cnf_tseitin = tseitin_encoding(cnf, len(cnf))
        return solve(cnf_tseitin, None)
    
    m = random.randint(5, 30)
    cnf = generate_cnf(m)
    min_order_val = min_order(cnf)
    proof_length_val = proof_length(cnf)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_val,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": abs(min_order_val - proof_length_val) < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.3 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.3)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")