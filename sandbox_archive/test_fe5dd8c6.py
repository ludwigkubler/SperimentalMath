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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Ensure at least 10*n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def cnf_to_kneser_graph(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        n = len(variables)
        graph = {i: [] for i in range(n)}
        for clause in cnf:
            for i in range(n):
                if (i + 1) not in [abs(lit) for lit in clause]:
                    continue
                for j in range(i + 1, n):
                    if (j + 1) not in [abs(lit) for lit in clause]:
                        graph[i].append(j)
                        graph[j].append(i)
        return graph
    
    def automorphism_group(graph):
        nodes = list(graph.keys())
        n = len(nodes)
        perm = list(range(n))
        visited = set()
        
        def dfs(node, new_node):
            if node in visited:
                return True
            visited.add(node)
            for neighbor in graph[node]:
                if new_node not in [perm[i] for i in range(len(perm)) if perm[i] == neighbor]:
                    return False
                if not dfs(neighbor, perm[new_node]):
                    return False
            return True
        
        def find_permutations():
            nonlocal perm
            while True:
                found = False
                for node in nodes:
                    new_node = random.choice(nodes)
                    if new_node != node and dfs(node, new_node):
                        perm[node], perm[new_node] = perm[new_node], perm[node]
                        found = True
                if not found:
                    break
        
        find_permutations()
        return perm
    
    def count_distinct_permutations(perm):
        n = len(perm)
        visited = set()
        
        def dfs(node, path):
            if node in visited:
                return 1
            visited.add(node)
            count = 0
            for neighbor in graph[node]:
                if neighbor not in path:
                    count += dfs(neighbor, path + [neighbor])
            visited.remove(node)
            return count
        
        total_count = 0
        for i in range(n):
            total_count += dfs(i, [i])
        return total_count
    
    def min_degree(graph):
        return min(len(neighbors) for neighbors in graph.values())
    
    def num_satisfying_assignments(cnf):
        n = len(cnf)
        count = 0
        for i in range(1 << n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if all(any(lit == 0 or lit == -assignment[abs(lit) - 1] for lit in clause) for clause in cnf):
                count += 1
        return count
    
    n_max = 40
    instances_tested = 0
    total_permutations = 0
    total_degrees = 0
    total_satisfying_assignments = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        graph = cnf_to_kneser_graph(cnf)
        perm = automorphism_group(graph)
        permutations = count_distinct_permutations(perm)
        degree = min_degree(graph)
        satisfying_assignments = num_satisfying_assignments(cnf)
        
        total_permutations += permutations
        total_degrees += degree
        total_satisfying_assignments += satisfying_assignments
        instances_tested += 1
    
    metric_value = total_permutations / instances_tested
    conjecture_holds = (metric_value <= n_max**2 * math.log(n_max)) and (total_degrees >= 2**n_max - total_satisfying_assignments)
    
    return {
        "metric_name": "Number of distinct permutations",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Permutations: {total_permutations}, Degree: {total_degrees}, Satisfying Assignments: {total_satisfying_assignments}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")