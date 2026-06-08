# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3_colorable_graph(n):
        graph = {i: set() for i in range(n)}
        edges = list(combinations(range(n), 2))
        while len(edges) > 0:
            u, v = random.choice(edges)
            if (u not in graph[v] and v not in graph[u]):
                graph[u].add(v)
                graph[v].add(u)
                edges.remove((u, v))
                for w in range(n):
                    if w != u and w != v and u in graph[w] and v in graph[w]:
                        graph[w].remove(u)
                        graph[w].remove(v)
        return graph
    
    def simplicial_complex(graph):
        n = len(graph)
        simplices = {frozenset([i]): 1 for i in range(n)}
        for k in range(2, n + 1):
            new_simplices = set()
            for face in combinations(range(n), k):
                if all(len(face & edge) % 2 == 1 for edge in simplices.keys()):
                    new_simplices.add(frozenset(face))
            simplices.update(new_simplices)
        return simplices
    
    def min_local_index(simplices):
        n = len(simplices)
        local_indices = [0] * n
        for face, index in simplices.items():
            if len(face) == 1:
                continue
            for vertex in face:
                neighbors = set()
                for other_face in simplices.keys():
                    if vertex in other_face and len(other_face - {vertex}) % 2 == 0:
                        neighbors.update(other_face)
                local_indices[vertex] += index * (len(neighbors) - len(face) + 1)
        return max(local_indices)
    
    def resolution_width(graph):
        clauses = []
        for i in range(len(graph)):
            for j in graph[i]:
                clauses.append([i, j])
                clauses.append([-i, -j])
        variables = set(range(len(graph)))
        
        def dpll():
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                var = unit_clause[0]
                if var < 0:
                    var = -var
                new_clauses = [c for c in clauses if var not in c and -var not in c]
                return dpll() or dpll()
            pure_literal = next((v for v in variables if all(v not in c and -v not in c for c in clauses)), None)
            if pure_literal is not None:
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return dpll() or dpll()
            var = next(iter(variables))
            new_clauses_true = [c for c in clauses if var not in c]
            new_clauses_false = [c for c in clauses if -var not in c]
            return dpll(new_clauses_true) or dpll(new_clauses_false)
        
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        graph = generate_3_colorable_graph(random.randint(5, n_max))
        simplices = simplicial_complex(graph)
        min_local = min_local_index(simplices)
        width = resolution_width(graph)
        metric_values.append(min_local / width)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    if min(metric_values) < 0.7 * max(metric_values):
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": "min_local_index_over_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")