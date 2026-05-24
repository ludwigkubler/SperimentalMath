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

def min_rank(graph):
    n = len(graph)
    A = [[graph[i][j] * graph[k][l] for l in range(n)] for k in range(n) for j in range(n)]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    return gaussian_elimination(A)

def resolution_length(graph):
    n = len(graph)
    clauses = []
    
    def add_clause(clause):
        clauses.append(clause)
    
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                add_clause([-i - 1, -j - 1])
                add_clause([i + 1, j + 1])
                add_clause([-i - 1, j + 1])
                add_clause([i + 1, -j - 1])
    
    def is_satisfiable():
        stack = []
        assignment = {}
        
        def backtrack():
            if len(stack) == len(clauses):
                return True
            literal = next((lit for lit in range(1, n + 1) if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return False
            
            stack.append(literal)
            assignment[literal] = True
            while stack:
                lit = stack[-1]
                satisfied = any(any(clause[i] == 0 for i, val in enumerate(assignment) if val) for clause in clauses)
                if not satisfied:
                    del assignment[lit]
                    stack.pop()
                    if -lit in assignment:
                        del assignment[-lit]
                    else:
                        return backtrack()
                else:
                    break
            return True
        
        return backtrack()
    
    return len(clauses) if is_satisfiable() else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    MinRank_G_tensor_G = min_rank(graph) ** 2
    ResolutionLength_T_G = resolution_length(graph)
    
    metric_value = MinRank_G_tensor_G / ResolutionLength_T_G if ResolutionLength_T_G > 0 else float('inf')
    conjecture_holds = metric_value >= 2
    counterexample = "" if conjecture_holds else f"Graph with n={n}, MinRank(G ⊗ G)={MinRank_G_tensor_G}, ResolutionLength(T_G)={ResolutionLength_T_G}"
    
    return {
        "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[0]['instances_tested']}, MinRank(G ⊗ G)={results[0]['metric_value']}, ResolutionLength(T_G)={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")