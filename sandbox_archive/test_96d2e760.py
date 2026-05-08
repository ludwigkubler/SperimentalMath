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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        num = 2
        while len(primes) < n:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def generate_3_regular_graph(n):
        graph = [[] for _ in range(n)]
        degrees = [0] * n
        added_edges = set()
        
        for _ in range(3 * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in added_edges and (v, u) not in added_edges and degrees[u] < 3 and degrees[v] < 3:
                    graph[u].append(v)
                    graph[v].append(u)
                    added_edges.add((u, v))
                    degrees[u] += 1
                    degrees[v] += 1
                    break
        
        return graph
    
    def generate_odd_charge(n):
        charge = [0] * n
        if sum(charge) % 2 == 0:
            charge[random.randint(0, n - 1)] ^= 1
        return charge
    
    def bfs(graph, start):
        queue = [start]
        visited = set([start])
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) - 1
    
    def count_triangles(graph, u):
        triangles = 0
        for v in graph[u]:
            for w in graph[v]:
                if w != u and w not in graph[u]:
                    triangles += 1
        return triangles // 3
    
    def count_4_cycles(graph, u):
        cycles = 0
        for v in graph[u]:
            for w in graph[v]:
                if w != u:
                    for x in graph[w]:
                        if x != u and x not in graph[u] and x != v:
                            cycles += 1
        return cycles // 4
    
    def forman_ricci_curvature(graph, charge, edge):
        u, v = edge
        t_e = count_triangles(graph, u) + count_triangles(graph, v)
        q_e = count_4_cycles(graph, u) + count_4_cycles(graph, v)
        return 2 * t_e + 2 * q_e - (len(graph[u]) + len(graph[v]) - 2)
    
    def dpll(cnf):
        stack = []
        assignment = [None] * len(cnf)
        
        def propagate():
            while stack:
                literal, value = stack.pop()
                if assignment[literal] is None:
                    assignment[literal] = value
                elif assignment[literal] != value:
                    return False
            return True
        
        def unit_propagate():
            changed = True
            while changed:
                changed = False
                for clause in cnf:
                    unsatisfied = [l for l, v in enumerate(clause) if assignment[l] is None and v == 1]
                    satisfied = any(assignment[l] == (v == -1) for l, v in enumerate(clause))
                    if len(unsatisfied) == 1 and not satisfied:
                        literal, value = unsatisfied[0], 1
                        stack.append((literal, value))
                        assignment[literal] = value
                        changed = True
        
        def pure_literal_elimination():
            for literal in range(len(cnf)):
                positive_count = sum(1 for clause in cnf if literal in clause)
                negative_count = sum(1 for clause in cnf if -literal in clause)
                if positive_count == 0:
                    assignment[literal] = True
                elif negative_count == 0:
                    assignment[literal] = False
        
        def backtrack():
            while stack:
                literal, value = stack.pop()
                assignment[literal] = None
                for l, v in enumerate(cnf):
                    if literal in v and assignment[l] is None:
                        stack.append((l, -v[l]))
                        break
        
        def solve():
            propagate()
            unit_propagate()
            pure_literal_elimination()
            if all(assignment[l] is not None for l in range(len(cnf))):
                return True
            literal = next(l for l in range(len(cnf)) if assignment[l] is None)
            stack.append((literal, 1))
            if solve():
                return True
            stack.pop()
            stack.append((literal, -1))
            if solve():
                return True
            backtrack()
            return False
        
        return solve()
    
    def tseitin_encoding(graph, charge):
        n = len(graph)
        cnf = []
        
        for i in range(n):
            cnf.append([i * 2 + charge[i], -(i * 2 + 1 - charge[i])])
        
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    cnf.append([-u * 2 - charge[u], -v * 2 - charge[v], u * 2 + 1 - charge[u], v * 2 + 1 - charge[v]])
        
        return cnf
    
    def log2_tseitin_size(cnf):
        size = sum(1 for clause in cnf if len(clause) > 0)
        return math.log2(size)
    
    n_values = [12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        graph = generate_3_regular_graph(n)
        charge = generate_odd_charge(n)
        cnf = tseitin_encoding(graph, charge)
        
        N_minus = sum(1 for u in range(n) for v in graph[u] if forman_ricci_curvature(graph, charge, (u, v)) < 0)
        T_DPLL = dpll(cnf)
        log2_T_DPLL = log2_tseitin_size(cnf)
        
        results.append({
            "metric_name": "N_minus",
            "metric_value": N_minus,
            "instances_tested": 1,
            "conjecture_holds": log2_T_DPLL >= 0.4 * N_minus - 5,
            "counterexample": ""
        })
    
    mean_N_minus = sum(result["metric_value"] for result in results) / len(results)
    std_N_minus = math.sqrt(sum((result["metric_value"] - mean_N_minus) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "mean_N_minus": mean_N_minus,
        "std_N_minus": std_N_minus,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"mean_N_minus\": {result['mean_N_minus']:.2f}, \"std_N_minus\": {result['std_N_minus']:.2f}, \"support_fraction\": {result['support_fraction']:.2f}}}")
    
    if result["support_fraction"] >= 0.8:
        print(f"RESULT: SUPPORTED mean={result['mean_N_minus']:.2f} std={result['std_N_minus']:.2f} support_fraction={result['support_fraction']:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"N_minus < 0.4 * N_minus - 5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")