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
    
    def generate_tseitin_formula(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append(f"p{i}")
        for i in range(1, n + 1):
            clauses.append(f"-p{i} p{i}")
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                clauses.append(f"p{i} -p{j} p{i}")
        return clauses
    
    def generate_graph(clauses):
        graph = {}
        for clause in clauses:
            if clause[0] == 'p':
                u = int(clause[1:]) - 1
                if u not in graph:
                    graph[u] = []
            elif clause[0] == '-':
                u = int(clause[2:]) - 1
                if u not in graph:
                    graph[u] = []
        for clause in clauses:
            if clause[0] == 'p':
                u = int(clause[1:]) - 1
                for v in range(n):
                    if v != u and (f"-p{v+1}" not in clauses or f"p{v+1}" not in clauses):
                        graph[u].append(v)
            elif clause[0] == '-':
                u = int(clause[2:]) - 1
                for v in range(n):
                    if v != u and (f"-p{v+1}" in clauses or f"p{v+1}" in clauses):
                        graph[u].append(v)
        return graph
    
    def find_loops(graph):
        loops = set()
        visited = [False] * n
        stack = []
        
        def dfs(node, parent):
            if visited[node]:
                loop = [node]
                while stack[-1] != node:
                    loop.append(stack.pop())
                loop.append(stack.pop())
                loops.update(loop)
                return True
            visited[node] = True
            stack.append(node)
            for neighbor in graph.get(node, []):
                if dfs(neighbor, node):
                    return True
            stack.pop()
            visited[node] = False
            return False
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return loops
    
    def resolution_proof_length(clauses):
        clauses_set = set(clauses)
        proof = []
        
        while True:
            new_clauses = []
            for clause in clauses:
                if '-' in clause:
                    literal = clause[2:]
                    if literal in clauses_set:
                        continue
                    new_clause = [l for l in clause if l != '-' + literal]
                    if not new_clause:
                        return len(proof)
                    new_clauses.append(new_clause)
            if not new_clauses:
                return len(proof)
            clauses.extend(new_clauses)
            proof.append(clauses[-1])
    
    n = 20
    clauses = generate_tseitin_formula(n)
    graph = generate_graph(clauses)
    loops = find_loops(graph)
    loop_count = len(loops)
    
    if loop_count == 0:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No loops in the graph"
        }
    
    proof_length = resolution_proof_length(clauses)
    expected_bound = 2 ** (math.ceil(math.log(loop_count, 2)))
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= expected_bound * 1.5 and proof_length >= expected_bound / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break