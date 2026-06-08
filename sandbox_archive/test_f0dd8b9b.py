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
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}, model=[]):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(assignment) + 1) if l not in assignment and -l not in assignment), None)
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
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack():
            nonlocal assignment, model
            last_literal = model[-1]
            del model[-1]
            del assignment[last_literal]
            return dpll(cnf, assignment, model)
        
        if propagate(literal):
            assignment[literal] = True
            model.append(literal)
            if dpll(cnf, assignment, model):
                return True
            backtrack()
        
        if propagate(-literal):
            assignment[-literal] = True
            model.append(-literal)
            if dpll(cnf, assignment, model):
                return True
            backtrack()
        
        return False
    
    def local_index(cnf):
        n = len(cnf)
        G = [[] for _ in range(n)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    u, v = abs(clause[i]) - 1, abs(clause[j]) - 1
                    G[u].append(v)
                    G[v].append(u)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in G[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        visited = [False] * n
        dfs(0, visited)
        return sum(1 for v in visited if v)
    
    def frege_depth(cnf):
        return len(dpll(cnf))
    
    results = []
    for n in range(5, 41):
        for _ in range(30):
            cnf = generate_cnf(n)
            li = local_index(cnf)
            fd = frege_depth(cnf)
            if fd == 0:
                continue
            ratio = li / fd
            results.append((n, li, fd, ratio))
    
    total_ratio = sum(ratio for _, _, _, ratio in results)
    mean_ratio = total_ratio / len(results)
    std_ratio = math.sqrt(sum((ratio - mean_ratio) ** 2 for _, _, _, ratio in results) / len(results))
    
    support_fraction = sum(1 for _, _, _, ratio in results if abs(ratio - (math.log(2) ** li)) < 2 ** li) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_index_to_frege_depth_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_conjecture")