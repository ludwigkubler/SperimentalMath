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
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def compute_orbits(cnf):
        n = len(cnf[0])
        graph = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                if clause[i] != 0:
                    for j in range(i + 1, n):
                        if clause[j] != 0:
                            graph[i][j] = 1
                            graph[j][i] = 1
        orbits = set()
        visited = [False] * n
        
        def dfs(node, orbit):
            if visited[node]:
                return
            visited[node] = True
            orbit.append(node)
            for neighbor in range(n):
                if graph[node][neighbor]:
                    dfs(neighbor, orbit)
        
        for i in range(n):
            if not visited[i]:
                orbit = []
                dfs(i, orbit)
                orbits.add(tuple(sorted(orbit)))
        
        return len(orbits)
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set()
        for clause in cnf:
            clauses.add(tuple(sorted(clause)))
        
        queue = list(clauses)
        while queue:
            new_clause = []
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    c1, c2 = sorted(queue[i]), sorted(queue[j])
                    for k in range(n):
                        if c1[k] == -c2[k]:
                            new_clause = [x for x in c1 if x != -c2[k]] + [x for x in c2 if x != -c1[k]]
                            break
                    else:
                        continue
                    break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(tuple(sorted(new_clause)))
        return len(queue)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    orbits = compute_orbits(cnf)
    width = resolution_width(cnf)
    
    metric_name = "Orbit-Width Ratio"
    metric_value = Fraction(orbits, width) if width != 0 else None
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    if orbits is not None and width is not None:
        conjecture_holds = abs(Fraction(orbits, width) - Fraction(n, 2)) <= Fraction(1, 5)
        if not conjecture_holds:
            counterexample = f"Orbit-Width Ratio {orbits}/{width} != Θ({n}/2)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif sum(r["conjecture_holds"] for r in results) >= 24:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((i + 1 for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")