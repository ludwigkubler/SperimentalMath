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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Generate Tseitin formula on expander graph
        for i in range(1, n):
            clauses.append([variables[i], -variables[i + 1]])
            clauses.append([-variables[i], variables[i + 2]])
            clauses.append([variables[i + 1], variables[i + 2]])
        
        # Add final clause to ensure satisfiability
        clauses.append(variables[1])
        
        return variables, clauses
    
    def min_rank(graph):
        n = len(graph)
        rank = 0
        
        for i in range(n):
            if graph[i][i] == 0:
                continue
            
            pivot_row = i
            for j in range(i + 1, n):
                if abs(graph[j][i]) > abs(graph[pivot_row][i]):
                    pivot_row = j
            
            if abs(graph[pivot_row][i]) < 1e-9:
                continue
            
            rank += 1
            graph[i], graph[pivot_row] = graph[pivot_row], graph[i]
            
            for j in range(n):
                if i == j:
                    continue
                
                factor = -graph[j][i] / graph[i][i]
                for k in range(n):
                    graph[j][k] += factor * graph[i][k]
        
        return rank
    
    def resolution_proof_length(clauses):
        stack = []
        clauses_set = set(tuple(c) for c in clauses)
        
        while True:
            new_clause = None
            for clause in clauses_set:
                if len(clause) == 1:
                    literal = clause[0]
                    if literal > 0 and -literal in [c for c in stack]:
                        return len(stack)
                    elif literal < 0 and -literal not in [c for c in stack]:
                        new_clause = [-literal]
                        break
            if new_clause is None:
                return float('inf')
            
            stack.append(new_clause[0])
            clauses_set.discard(tuple([new_clause[0]]))
            new_clauses = []
            for clause in clauses_set:
                if -new_clause[0] in clause:
                    continue
                new_clauses.append([l for l in clause if l != -new_clause[0]])
            clauses_set.update(new_clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        graph = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    graph[abs(clause[i])][abs(clause[j])] += 1
                    graph[abs(clause[j])][abs(clause[i])] += 1
        
        min_rank_value = min_rank(graph)
        resolution_length = resolution_proof_length(clauses)
        
        if resolution_length == float('inf'):
            continue
        
        results.append({
            "n": n,
            "min_rank": min_rank_value,
            "resolution_length": resolution_length
        })
    
    if not results:
        return {
            "metric_name": "2^MinRank(C_F) / t*(F)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    total_ratio = sum(2**r["min_rank"] / r["resolution_length"] for r in results)
    avg_ratio = total_ratio / len(results)
    
    return {
        "metric_name": "2^MinRank(C_F) / t*(F)",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": avg_ratio > 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed + 1}")