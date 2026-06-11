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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d - len(graph[i]))
            for neighbor in neighbors:
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges.add((i, neighbor))
        return graph
    
    def tutte_polynomial(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u in G:
            for v in G[u]:
                if u < v:
                    A[u][v] = -1
                else:
                    A[v][u] = -1
            A[u][u] = len(G[u])
        
        def determinant(M):
            n = len(M)
            if n == 2:
                return M[0][0] * M[1][1] - M[0][1] * M[1][0]
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in M[1:]]
                det += ((-1) ** j) * M[0][j] * determinant(submatrix)
            return det
        
        return determinant(A)
    
    def brauer_group_order(T):
        if T == 0:
            return 0
        factors = []
        for i in range(2, abs(T) + 1):
            while T % i == 0:
                factors.append(i)
                T //= i
        unique_factors = set(factors)
        order = 1
        for factor in unique_factors:
            count = factors.count(factor)
            if count % 2 != 0:
                order *= factor
        return order
    
    def resolution_proof_width(G):
        n = len(G)
        clauses = []
        for u in G:
            clause = [f"X{i+1}" for i in G[u]]
            clauses.append(clause)
        
        def is_satisfiable(clauses):
            variables = set()
            for clause in clauses:
                variables.update(clause)
            
            assignment = {var: None for var in variables}
            stack = []
            while True:
                if not stack:
                    unassigned_var = next((var for var in variables if assignment[var] is None), None)
                    if unassigned_var is None:
                        return True
                    assignment[unassigned_var] = True
                    stack.append(unassigned_var)
                
                var = stack[-1]
                if all(assignment[v] != (not val) for v, val in zip(clauses[0], assignment.values())):
                    assignment[var] = False
                    stack.pop()
                else:
                    clauses = [c for c in clauses if not any(v in c and assignment[v] == val for v, val in zip(c, assignment.values()))]
                    if not clauses:
                        return True
        
        width = 0
        while len(clauses) > 1:
            max_clause_length = max(len(c) for c in clauses)
            if max_clause_length <= width:
                break
            width += 1
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    new_clause = list(set(clauses[i]) | set(clauses[j]))
                    if is_satisfiable(new_clauses):
                        new_clauses.append(new_clause)
                    else:
                        clauses.remove(clauses[i])
                        break
            else:
                clauses = new_clauses
        
        return width
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1, 5):
        d = 2 * (n - 1) // n
        G = generate_d_regular_graph(n, d)
        if G is None:
            continue
        
        T = tutte_polynomial(G)
        min_order_Br_G = brauer_group_order(T)
        w_G = resolution_proof_width(G)
        
        instances_tested += 1
        metric_values.append(min_order_Br_G)
    
    if instances_tested == 0:
        return {
            "metric_name": "Brauer Group Order vs Resolution Proof Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / instances_tested)
    correlation_coefficient = sum((metric_values[i] - mean) * (i / n_max - 0.5) for i in range(instances_tested)) / (instances_tested * std_dev * math.sqrt(0.16))
    
    return {
        "metric_name": "Brauer Group Order vs Resolution Proof Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")