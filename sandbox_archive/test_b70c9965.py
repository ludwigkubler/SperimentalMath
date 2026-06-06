# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        
        def dpll():
            if not cnf:
                return True
            literal = next((l for l in range(-n, n) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            new_cnf = []
            for clause in cnf:
                if any(l in assignment and assignment[l] for l in clause):
                    continue
                elif all(-l in assignment and not assignment[-l] for l in clause):
                    return False
                else:
                    new_clause = [l for l in clause if l != literal]
                    if -literal in new_clause:
                        new_clause.remove(-literal)
                    new_cnf.append(new_clause)
            stack.append((new_cnf, literal))
            result = dpll()
            if not result:
                del assignment[literal]
                stack.pop()
                assignment[-literal] = True
                for clause in cnf:
                    if any(l in assignment and assignment[l] for l in clause):
                        continue
                    elif all(-l in assignment and not assignment[-l] for l in clause):
                        return False
                    else:
                        new_clause = [l for l in clause if -l != literal]
                        if literal in new_clause:
                            new_clause.remove(literal)
                        new_cnf.append(new_clause)
                stack.append((new_cnf, -literal))
                result = dpll()
            if not result:
                del assignment[-literal]
                stack.pop()
            return result
        
        return dpll()
    
    def count_orbits(graph):
        n = len(graph)
        visited = [False] * n
        orbits = 0
        
        def dfs(node, color):
            nonlocal visited
            visited[node] = True
            for neighbor in range(n):
                if graph[node][neighbor] and not visited[neighbor]:
                    dfs(neighbor, color)
        
        for node in range(n):
            if not visited[node]:
                orbits += 1
                dfs(node, orbits)
        
        return orbits
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    graph = [[False] * n for _ in range(n)]
    for clause in cnf:
        for l1 in clause:
            for l2 in clause:
                if l1 != l2 and abs(l1) == abs(l2):
                    continue
                i, j = abs(l1) - 1, abs(l2) - 1
                graph[i][j] = True
                graph[j][i] = True
    
    orbits = count_orbits(graph)
    satisfiable = is_satisfiable(cnf)
    
    if not satisfiable:
        return {
            "metric_name": "Orbits",
            "metric_value": orbits,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Unsatisfiable CNF"
        }
    
    return {
        "metric_name": "Orbits",
        "metric_value": orbits,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r.get("conjecture_holds", False))
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif conjecture_holds_count >= 24:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r.get("conjecture_holds", False)), None)
        print(f"RESULT: FALSIFIED counterexample=\"Unsatisfiable CNF\" first_failing_seed={first_failing_seed}")