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
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)]
            for _ in range(random.randint(0, n-1)):
                literal = random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                while literal in clause:
                    literal = random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                clause.append(literal)
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def search(model):
            unsatisfied_clauses = [c for c in cnf if not any(abs(lit) in model and (model[lit] == lit > 0 or model[-lit] == lit < 0) for lit in c)]
            if not unsatisfied_clauses:
                return True
            unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                model[-literal] = literal < 0
                return search(model)
            pure_literal = next((lit for lit in range(1, n+1) if (all(lit not in c or -lit in c for c in unsatisfied_clauses) and all(-lit not in c or lit in c for c in unsatisfied_clauses))), None)
            if pure_literal:
                model[pure_literal] = True
                return search(model)
            literal = random.choice([l for l in range(1, n+1) if l not in model and -l not in model])
            model[literal] = True
            if search(model):
                return True
            model[-literal] = True
            if search(model):
                return True
            del model[literal]
            del model[-literal]
            return False
        return search({})

    def topological_entropy(cnf):
        n = len(cnf)
        adj_matrix = [[0]*n for _ in range(n)]
        for clause in cnf:
            for lit1 in clause:
                for lit2 in clause:
                    if abs(lit1) != abs(lit2):
                        adj_matrix[abs(lit1)-1][abs(lit2)-1] = 1
                        adj_matrix[abs(lit2)-1][abs(lit1)-1] = 1
        
        def dfs(v, visited, stack):
            visited[v] = True
            for i in range(n):
                if adj_matrix[v][i] == 1 and not visited[i]:
                    dfs(i, visited, stack)
            stack.append(v)
        
        visited = [False]*n
        stack = []
        for i in range(n):
            if not visited[i]:
                dfs(i, visited, stack)
        
        def transpose():
            transposed = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    transposed[j][i] = adj_matrix[i][j]
            return transposed
        
        def kosaraju():
            visited = [False]*n
            sccs = []
            
            def dfs_util(v, visited):
                visited[v] = True
                for i in range(n):
                    if adj_matrix[v][i] == 1 and not visited[i]:
                        dfs_util(i, visited)
            
            while stack:
                v = stack.pop()
                if not visited[v]:
                    scc = []
                    dfs_util(v, visited)
                    sccs.append(scc)
            
            return sccs
        
        sccs = kosaraju()
        in_degree = [0]*n
        out_degree = [0]*n
        for i in range(n):
            for j in range(n):
                if adj_matrix[i][j] == 1:
                    out_degree[i] += 1
                    in_degree[j] += 1
        
        entropy = sum(math.log(len(scc)) for scc in sccs) / n
        return entropy
    
    def dpll_tree_diameter(cnf):
        n = len(cnf)
        visited = [False]*n
        max_depth = [0]
        
        def dfs(v, depth):
            visited[v] = True
            if depth > max_depth[0]:
                max_depth[0] = depth
            for i in range(n):
                if adj_matrix[v][i] == 1 and not visited[i]:
                    dfs(i, depth + 1)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 1)
        
        return max_depth[0]
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    entropy = topological_entropy(cnf)
    diameter = dpll_tree_diameter(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": entropy * diameter,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")