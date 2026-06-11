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
    
    def generate_cnf(n: int):
        cnf = []
        for _ in range(random.randint(1, 2**n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit not in clause and -lit not in clause for lit in cnf):
                cnf.append(clause)
        return cnf
    
    def dpll_search_tree_width(cnf):
        n = len(cnf[0])
        assignment = [None] * (n + 1)
        
        def is_satisfiable(assignment, clause):
            return any(lit in assignment and assignment[lit] == sign for lit, sign in enumerate(clause))
        
        def dpll(cnf, level):
            if not cnf:
                return True
            literal = next((lit for lit in range(1, n + 1) if assignment[lit] is None), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if dpll(new_cnf, level + 1):
                return True
            assignment[literal] = False
            
            assignment[-literal] = True
            new_cnf = [c for c in cnf if -literal not in c and literal not in c]
            if dpll(new_cnf, level + 1):
                return True
            assignment[-literal] = None
            
            return False
        
        return dpll(cnf, 0)
    
    def quandle_order(cnf):
        n = len(cnf[0])
        truth_table = [[False] * (2 ** n) for _ in range(n)]
        
        def evaluate_clause(clause, assignment):
            return any(lit in assignment and assignment[lit] == sign for lit, sign in enumerate(clause))
        
        for i in range(1 << n):
            assignment = [None if bit == 0 else -1 if bit == 2 else 1 for bit in format(i, f'0{n}b')]
            for clause in cnf:
                truth_table[clause.index(lit) if lit > 0 else -clause.index(-lit)][i] = evaluate_clause(clause, assignment)
        
        order = 0
        while True:
            found = False
            for i in range(n):
                new_truth_table = [[False] * (2 ** n) for _ in range(n)]
                for j in range(2 ** n):
                    if truth_table[i][j]:
                        for k in range(n):
                            if truth_table[k][j]:
                                new_truth_table[k][(j ^ (1 << i)) % (2 ** n)] = True
                if new_truth_table != truth_table:
                    found = True
                    truth_table = new_truth_table
            if not found:
                break
            order += 1
        
        return order
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    orders = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = dpll_search_tree_width(cnf)
        order = quandle_order(cnf)
        widths.append(width)
        orders.append(order)
    
    correlation = pearson_correlation(orders, widths)
    support_fraction = sum(correlation >= 0.5 for _ in range(30)) / 30
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "correlation < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")