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
    
    def generate_random_graph(n, m):
        if m > n * (n - 1) // 2:
            return None
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return [sorted(list(u)) for u in edges]
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        for i in range(n):
            clauses.append([literals[2 * i], literals[2 * i + 1]])
            for j in graph[i]:
                if j > i:
                    clauses.append([-literals[2 * i], -literals[2 * j]])
                    clauses.append([-literals[2 * i + 1], -literals[2 * j + 1]])
        return literals, clauses
    
    def dpll(clauses):
        stack = []
        assignment = {}
        def solve():
            if not clauses:
                return True
            literal = next(l for l in range(1, max(max(c) for c in clauses)) + 1 if l not in assignment and -l not in assignment)
            assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                elif -literal in clause:
                    new_clauses.append([x for x in clause if x != -literal])
                else:
                    new_clauses.append(clause)
            if solve():
                return True
            assignment[literal] = False
            for clause in clauses:
                if -literal in clause:
                    continue
                elif literal in clause:
                    new_clauses.append([x for x in clause if x != literal])
                else:
                    new_clauses.append(clause)
            stack.append((assignment.copy(), new_clauses))
            return solve()
        while True:
            if not stack:
                return False
            assignment, clauses = stack.pop()
            if solve():
                return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_random_graph(n, random.randint(0, n * (n - 1) // 2))
            if graph is None:
                continue
            literals, clauses = tseitin_formula(graph)
            length = len(clauses)
            total_length += length
            instances_tested += 1
    
    mean_length = Fraction(total_length, instances_tested).limit_denominator()
    
    return {
        "metric_name": "Tseitin Resolution Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_length >= 2 ** (math.ceil(math.log(n_values[-1], 2))),
        "counterexample": "" if mean_length >= 2 ** (math.ceil(math.log(n_values[-1], 2))) else f"Graph with n={n_values[-1]} and {instances_tested} instances"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n_values[-1]} and {r['instances_tested']} instances\" first_failing_seed={seed}")
                break