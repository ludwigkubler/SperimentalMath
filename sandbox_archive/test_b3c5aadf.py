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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literals = {}
        for c in clauses:
            pos, neg = 0, 0
            for l in c:
                if l > 0:
                    pos += 1
                else:
                    neg += 1
            if pos == len(c):
                pure_literals[l] = True
            elif neg == len(c):
                pure_literals[-l] = False
        if pure_literals:
            literal, value = next(iter(pure_literals.items()))
            new_assignment[literal] = value
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pivot = random.choice(clauses[0])
        new_assignment[pivot] = True
        if dpll([c for c in clauses if pivot not in c and -pivot not in c], new_assignment):
            return True
        new_assignment[pivot] = False
        new_assignment[-pivot] = True
        return dpll([c for c in clauses if -pivot not in c and pivot not in c], new_assignment)
    
    def clause_graph(clauses):
        n = max(abs(l) for l in set.union(*map(set, clauses)))
        G = [[] for _ in range(n + 1)]
        for c in clauses:
            for i in range(len(c)):
                for j in range(i + 1, len(c)):
                    G[abs(c[i])].append(abs(c[j]))
                    G[abs(c[j])].append(abs(c[i]))
        return G
    
    def normalize(G):
        n = len(G)
        visited = [False] * (n + 1)
        stack = []
        
        def dfs(v):
            if not visited[v]:
                visited[v] = True
                for u in G[v]:
                    dfs(u)
                stack.append(v)
        
        for v in range(1, n + 1):
            dfs(v)
        
        component = [0] * (n + 1)
        comp_id = 0
        
        def bfs(start):
            nonlocal comp_id
            queue = [start]
            visited[start] = True
            while queue:
                v = queue.pop(0)
                component[v] = comp_id
                for u in G[v]:
                    if not visited[u]:
                        visited[u] = True
                        queue.append(u)
            comp_id += 1
        
        visited = [False] * (n + 1)
        for v in range(n, 0, -1):
            if not visited[v]:
                bfs(v)
        
        return component
    
    def smallest_normalizing_set(G):
        n = len(G)
        component = normalize(G)
        normalizing_sets = [[] for _ in range(n)]
        
        for i in range(1, n + 1):
            normalizing_sets[component[i]].append(i)
        
        min_size = float('inf')
        for s in normalizing_sets:
            if len(s) < min_size:
                min_size = len(s)
        
        return min_size
    
    def generate_3sat(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, k=3)
            if random.choice([True, False]):
                clause = [-l for l in clause]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_height = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            clauses = generate_3sat(n, m)
            G = clause_graph(clauses)
            N_G = smallest_normalizing_set(G)
            
            if N_G == 0:
                continue
            
            height = dpll(clauses, {})
            total_height += height
            instances_tested += 1
            n_max = max(n_max, n)
            
            if abs(height - N_G) > 3 * N_G:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, h(DPLL)=<{height}, |N_G|={N_G}"
    
    mean_height = total_height / instances_tested if instances_tested > 0 else 0
    std_dev = math.sqrt(sum((h - mean_height) ** 2 for h in range(total_height)) / instances_tested) if instances_tested > 1 else 0
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_height) ** 2 for r in results)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")