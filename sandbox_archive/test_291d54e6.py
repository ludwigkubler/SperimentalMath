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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = {}
        clauses = []
        
        def literal(i):
            if i not in literals:
                literals[i] = len(literals) + 1
            return literals[i]
        
        def negate(x):
            return -x
        
        def binary_op(x, y, op):
            if x > 0 and y > 0:
                new_literal = max(literals.values()) + 1
                clauses.append([negate(new_literal), negate(x), negate(y)])
                clauses.append([new_literal, x, y])
                return new_literal
            elif x < 0 and y < 0:
                return binary_op(negate(x), negate(y), op)
            else:
                if op == 'and':
                    return negate(binary_op(-x, -y, 'or'))
                elif op == 'or':
                    return negate(binary_op(-x, -y, 'and'))
        
        def parse_expression(i):
            if i < 0:
                return negate(parse_expression(-i))
            else:
                return literal(i)
        
        for i in range(n):
            clauses.append([literal(2**i), parse_expression(f[2**(i+1) - 2**i])])
        
        for j in range(1, n):
            for i in range(j):
                clauses.append([literal(2**(i+j)), binary_op(parse_expression(f[2**(i+j) - 2**i]), parse_expression(f[2**(i+j) - 2**j]), 'or')])
        
        return clauses
    
    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = set(abs(x) for x in clauses[i])
                    clause_j = set(abs(x) for x in clauses[j])
                    common_literals = clause_i & clause_j
                    if not common_literals:
                        continue
                    
                    new_clause = []
                    for lit in clause_i:
                        if -lit not in clause_j:
                            new_clause.append(lit)
                    for lit in clause_j:
                        if -lit not in clause_i:
                            new_clause.append(lit)
                    
                    if len(new_clause) == 0:
                        return True
                    
                    new_clauses.append(new_clause)
            
            if new_clauses == clauses:
                return False
            clauses = new_clauses
    
    def algebraic_degree(f, n):
        degree = 0
        for i in range(2**n):
            if f[i] == 1:
                degree += sum(1 for j in range(n) if (i & (1 << j)) != 0)
        return degree
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    phi_f = tseitin_formula(f, n)
    
    d_phi_f = resolution(phi_f)
    
    delta_f = algebraic_degree(f, n)
    
    if d_phi_f:
        return {
            "metric_name": "Correlation",
            "metric_value": 1.0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Correlation",
            "metric_value": -1.0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Unprovable by resolution"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Unprovable by resolution\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")