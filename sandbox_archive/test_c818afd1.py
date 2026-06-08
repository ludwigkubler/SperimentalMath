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
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u, neighbors in graph.items():
            clauses.append([literals[u]] + [-literals[v] for v in neighbors])
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    clauses.append([-literals[neighbors[i]], -literals[neighbors[j]]])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            for other_clause in clauses:
                if literal in other_clause:
                    new_clause = list(set(other_clause) - {literal})
                    if not new_clause:
                        return len(queue)
                    if new_clause not in learned_clauses and new_clause not in queue:
                        learned_clauses.append(new_clause)
                        queue.append(new_clause)
        return len(queue)
    
    def alexander_orlik_solomon_complexity(graph):
        n = len(graph)
        if n == 0:
            return 0
        generators = []
        for i in range(n):
            generator = [1] * n
            generator[i] = -1
            generators.append(generator)
        return len(generators)
    
    def run_dpll(clauses):
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0:
                    literal = -literal
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
            pure_literal = next((l for l in range(1, n + 1) if (all(l in c or -l in c for c in clauses)) != all(-l in c or l in c for c in clauses)), None)
            if pure_literal is not None:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
            literal, _ = random.choice(clauses)
            return dpll(clauses + [[-literal]], assignment) or dpll(clauses + [[literal]], assignment)
        n = len(clauses)
        assignment = [False] * (n + 1)
        return dpll(clauses, assignment)
    
    def run_trial(seed: int):
        random.seed(seed)
        
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            return {"metric_name": "resolution_width", "metric_value": float('inf'), "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "invalid_d_regular_graph"}
        
        literals, clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        
        aos_complexity = alexander_orlik_solomon_complexity(graph)
        
        return {"metric_name": "resolution_width", "metric_value": width, "instances_tested": 1, "n_max": n, "conjecture_holds": abs(aos_complexity - width) <= 10 and aos_complexity / width <= 3 and width / aos_complexity <= 3, "counterexample": "" if aos_complexity / width <= 3 and width / aos_complexity <= 3 else f"AOS={aos_complexity}, Width={width}"}
    
    return run_trial(seed)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("metric_value" in r and not math.isinf(r["metric_value"]) for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")