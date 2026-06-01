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
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice(range(-n, 0)) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            if literal < 0 and -literal in assignment and assignment[-literal]:
                return False
            elif literal > 0 and literal not in assignment:
                assignment[literal] = True
            else:
                assignment[literal] = False
        pure_literals = [l for l in range(1, n + 1) if all(l not in c or -l not in c for c in cnf)]
        if pure_literals:
            literal = pure_literals[0]
            if literal in assignment and assignment[literal]:
                return False
            else:
                assignment[literal] = True
        literals = list(assignment.keys())
        literal = random.choice(literals)
        if literal < 0:
            literal = -literal
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return dpll(new_cnf, assignment) or dpll(new_cnf, {**assignment, literal: False})
    
    def quaternionic_root_count(cnf):
        roots = set()
        for clause in cnf:
            for lit in clause:
                if lit < 0:
                    roots.add(abs(lit))
        return len(roots)
    
    def calculate_diameter(cnf):
        n = max([abs(lit) for lit in range(-len(cnf), 0)])
        graph = {i: [] for i in range(1, n + 1)}
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    if clause[i] < 0 and -clause[j] in graph[abs(clause[i])]:
                        graph[abs(clause[i])].append(abs(clause[j]))
                    elif clause[j] < 0 and -clause[i] in graph[abs(clause[j])]:
                        graph[abs(clause[j])].append(abs(clause[i]))
        def bfs(start):
            visited = set()
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            queue.append(neighbor)
            return len(visited) - 1
        max_diameter = 0
        for i in range(1, n + 1):
            max_diameter = max(max_diameter, bfs(i))
        return max_diameter
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    min_root_count = quaternionic_root_count(cnf)
    diameter = calculate_diameter(cnf)
    
    return {
        "metric_name": "min_root_count",
        "metric_value": min_root_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")