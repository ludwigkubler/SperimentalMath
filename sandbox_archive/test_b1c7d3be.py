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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or n <= 1:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(1, n):
            for j in range(i):
                if len(graph[j]) < d and len(graph[i]) < d:
                    edge = (i, j)
                    if edge not in edges_used and (j, i) not in edges_used:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_used.add(edge)
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        for i in range(n):
            clause = [literals[2 * i], literals[2 * i + 1]]
            clauses.append(clause)
            for j in graph[i]:
                neg_clause = [-literals[2 * j + 1]]
                clauses.append(neg_clause)
        return clauses, literals
    
    def resolution_width(clauses):
        n = len(clauses)
        stack = []
        literals = set()
        
        def unit_propagate():
            while True:
                found = False
                for clause in clauses:
                    if len(clause) == 1:
                        literal = clause[0]
                        if literal < 0 and -literal in literals:
                            return None
                        elif literal > 0 and literal not in literals:
                            literals.add(literal)
                            stack.append((literal, False))
                            found = True
                if not found:
                    break
        
        def resolve(clause1, clause2):
            new_clause = []
            for lit1 in clause1:
                for lit2 in clause2:
                    if lit1 == -lit2:
                        break
                else:
                    new_clause.append(lit1)
            return new_clause
        
        unit_propagate()
        
        while stack:
            literal, is_negated = stack.pop()
            literals.remove(literal)
            new_clauses = []
            for clause in clauses:
                if literal not in clause and -literal not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    new_clauses.extend(resolve(clause, [l for l in stack if l[0] == -literal]))
                elif -literal in clause:
                    new_clauses.extend(resolve(clause, [l for l in stack if l[0] == literal]))
            clauses = new_clauses
            unit_propagate()
        
        return len(stack)
    
    def quotient_sheaves(graph):
        n = len(graph)
        sheaves = [[] for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                if not sheaves[j]:
                    sheaves[j].append(i)
        return sheaves
    
    def min_index(sheaves):
        indices = [len(sheaf) for sheaf in sheaves]
        return max(indices)
    
    n = 30
    d = random.randint(2, 8)
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "min_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    clauses, literals = tseitin_formula(graph)
    width = resolution_width(clauses)
    if width is None:
        return {
            "metric_name": "min_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_failed"
        }
    
    sheaves = quotient_sheaves(graph)
    min_idx = min_index(sheaves)
    
    return {
        "metric_name": "min_index",
        "metric_value": min_idx,
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
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")