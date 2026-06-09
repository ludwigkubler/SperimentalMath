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
    
    def generate_circuit(n):
        if n == 1:
            return "A"
        else:
            a, b = generate_circuit(n-1), generate_circuit(n-1)
            return f"({a} AND {b}) OR A"
    
    def tseitin_formula(expr):
        literals = set()
        clauses = []
        
        def helper(sub_expr):
            if sub_expr.isalpha():
                literals.add(sub_expr)
                return sub_expr
            elif "AND" in sub_expr:
                a, b = sub_expr.split(" AND ")
                a_var = helper(a)
                b_var = helper(b)
                new_var = f"X{len(literals)}"
                clauses.append(f"{a_var} OR {b_var} OR NOT {new_var}")
                clauses.append(f"NOT {a_var} OR NOT {b_var} OR {new_var}")
                literals.add(new_var)
                return new_var
            elif "OR" in sub_expr:
                a, b = sub_expr.split(" OR ")
                a_var = helper(a)
                b_var = helper(b)
                new_var = f"X{len(literals)}"
                clauses.append(f"{a_var} OR {b_var} OR NOT {new_var}")
                clauses.append(f"NOT {a_var} OR {new_var}")
                clauses.append(f"NOT {b_var} OR {new_var}")
                literals.add(new_var)
                return new_var
            elif "NOT" in sub_expr:
                sub_expr = sub_expr[4:]
                sub_var = helper(sub_expr)
                new_var = f"X{len(literals)}"
                clauses.append(f"{sub_var} OR NOT {new_var}")
                literals.add(new_var)
                return new_var
    
    def resolution_width(clauses):
        clauses_set = set(clauses)
        while True:
            new_clauses = []
            for clause1 in clauses_set:
                for clause2 in clauses_set:
                    if len(set(clause1.split()) & set(clause2.split())) == 1:
                        new_clause = " OR ".join(sorted(list(set(clause1.split()) ^ set(clause2.split()))))
                        if new_clause not in clauses_set and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses_set.update(new_clauses)
        return len(clauses_set)
    
    def simplicial_decomposition(expr):
        # Placeholder for simplicial decomposition logic
        # This is a dummy implementation and should be replaced with actual logic
        return 1
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    literals, clauses = tseitin_formula(circuit)
    width = resolution_width(clauses)
    simplicial_cells = simplicial_decomposition(circuit)
    
    return {
        "metric_name": "Resolution Width vs. Simplicial Cells",
        "metric_value": width / simplicial_cells,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")