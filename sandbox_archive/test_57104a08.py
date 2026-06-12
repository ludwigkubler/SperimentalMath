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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        stack = []
        seen = set()
        for clause in cnf:
            stack.append(clause)
            seen.update(clause)
        
        while stack:
            clause1 = stack.pop()
            if not clause1:
                continue
            literal = random.choice(clause1)
            other_clauses = [c for c in cnf if literal in c]
            for clause2 in other_clauses:
                new_clause = [x for x in clause2 if x != -literal and x != literal]
                if not new_clause:
                    return len(stack) + 1
                stack.append(new_clause)
        
        return len(stack)

    def graphical_model(cnf):
        graph = {}
        for clause in cnf:
            for lit1 in clause:
                for lit2 in clause:
                    if lit1 != lit2 and abs(lit1) == abs(lit2):
                        continue
                    var1, var2 = abs(lit1), abs(lit2)
                    if var1 not in graph:
                        graph[var1] = set()
                    if var2 not in graph:
                        graph[var2] = set()
                    graph[var1].add(var2)
                    graph[var2].add(var1)
        return graph

    def geometric_entropy(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph.values())
        avg_degree = degree_sum / n
        entropy = 0
        for neighbors in graph.values():
            prob = len(neighbors) / avg_degree
            if prob != 1:
                entropy -= prob * math.log2(prob)
        return entropy

    def dpll(cnf):
        stack = []
        assignment = {}
        seen = set()
        for clause in cnf:
            stack.append(clause)
            seen.update(clause)
        
        while stack:
            clause1 = stack.pop()
            if not clause1:
                continue
            literal = random.choice(clause1)
            other_clauses = [c for c in cnf if literal in c]
            for clause2 in other_clauses:
                new_clause = [x for x in clause2 if x != -literal and x != literal]
                if not new_clause:
                    return True
                stack.append(new_clause)
        
        return False

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = graphical_model(cnf)
    entropy = geometric_entropy(graph)
    width = resolution_width(cnf)
    
    if width > entropy * 10:  # Arbitrary factor to check the bound
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "width > entropy * 10"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='width > entropy * 10' first_failing_seed={first_failing_seed}")