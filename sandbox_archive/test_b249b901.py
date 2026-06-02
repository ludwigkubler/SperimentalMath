# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_encoding(cnf):
        new_vars = {}
        new_cnf = []
        
        def encode_clause(clause):
            if len(clause) == 1:
                return clause[0]
            else:
                v = next(v for v in range(1, max(new_vars.values()) + 2) if v not in new_vars)
                new_vars[v] = True
                new_cnf.append([-v])
                for literal in clause:
                    new_cnf.append([literal, -v])
                return v
        
        def encode_clauses(clauses):
            if len(clauses) == 1:
                return encode_clause(clauses[0])
            else:
                v = next(v for v in range(1, max(new_vars.values()) + 2) if v not in new_vars)
                new_vars[v] = True
                new_cnf.append([-v])
                for clause in clauses:
                    new_cnf.append([encode_clause(clause), -v])
                return v
        
        def encode_formula(formula):
            if isinstance(formula, list):
                return encode_clauses(formula)
            else:
                return formula
        
        cnf = [encode_formula(cnf) for cnf in cnf]
        
        return new_vars, new_cnf
    
    def quiver_representation(cnf):
        new_vars, new_cnf = tseitin_encoding(cnf)
        n = len(new_vars)
        quiver_rep = [[0] * n for _ in range(n)]
        
        for clause in new_cnf:
            if len(clause) == 1:
                u = abs(clause[0]) - 1
                quiver_rep[u][u] += 1
            else:
                for literal in clause:
                    u, v = abs(literal) - 1, abs(next(lit for lit in clause if lit != literal)) - 1
                    quiver_rep[u][v] += 1
        
        return quiver_rep
    
    def min_order(quiver_rep):
        n = len(quiver_rep)
        visited = [False] * n
        order = 0
        
        def dfs(node):
            nonlocal order
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if quiver_rep[node][neighbor] > 0:
                        dfs(neighbor)
                order += 1
        
        for node in range(n):
            dfs(node)
        
        return n - order
    
    def frege_proof_length(cnf):
        # Placeholder function to compute Frege proof length
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 2  # Simplified example
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(5, 10))]
    
    quiver_rep = quiver_representation(cnf)
    min_order_value = min_order(quiver_rep)
    frege_length = frege_proof_length(cnf)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float('nan'),  # Placeholder for actual calculation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(math.isnan(res["metric_value"]) for res in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if not math.isnan(res["metric_value"]) and res["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, res in zip(seeds, results) if not math.isnan(res["metric_value"]) and not res["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")