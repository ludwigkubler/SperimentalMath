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
        if (n * d) % 2 != 0 or d < 1 or n < d + 1:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = 0
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0 and edges_added < (n * d) // 2:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges_added += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        
        for i in range(n):
            clause = [literals[2 * i - 1]]
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clause.append(-literals[2 * j - 1])
                    clause.append(-literals[2 * j])
                else:
                    clause.append(literals[2 * j - 1])
                    clause.append(literals[2 * j])
            clauses.append(clause)
        
        for i in range(1, n + 1):
            clauses.append([literals[2 * i - 1], literals[2 * i]])
            clauses.append([-literals[2 * i - 1], -literals[2 * i]])
        
        return clauses
    
    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        width = 0
        
        while queue:
            new_queue = []
            while queue:
                clause1 = queue.pop()
                for clause2 in learned_clauses + queue:
                    common = set(clause1).intersection(set(clause2))
                    if len(common) == 1:
                        new_clause = list(set(clause1 + clause2) - common)
                        if len(new_clause) > width:
                            width = len(new_clause)
                        new_queue.append(new_clause)
            queue, learned_clauses = new_queue, queue
        
        return width
    
    def diophantine_equations(graph):
        n = len(graph)
        equations = set()
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    equation = [f"x_{i+1} + x_{j+1} = 1"]
                    equations.add(tuple(sorted(equation)))
        
        return equations
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def generate_random_d_regular_graphs(d, max_n):
        graphs = []
        while len(graphs) < 30:
            n = random.randint(5, max_n)
            graph = generate_d_regular_graph(n, d)
            if graph is not None:
                graphs.append((n, graph))
        return graphs
    
    def main():
        d = 2
        max_n = 40
        graphs = generate_random_d_regular_graphs(d, max_n)
        
        diophantine_counts = []
        resolution_widths = []
        
        for n, graph in graphs:
            equations = diophantine_equations(graph)
            width = resolution_width(tseitin_formula(graph))
            
            if len(equations) == 0 or width == 0:
                continue
            
            diophantine_counts.append(len(equations))
            resolution_widths.append(width)
        
        if not diophantine_counts or not resolution_widths:
            return {
                "metric_name": "Pearson correlation",
                "metric_value": None,
                "instances_tested": len(diophantine_counts),
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        correlation = pearson_correlation(diophantine_counts, resolution_widths)
        
        return {
            "metric_name": "Pearson correlation",
            "metric_value": correlation,
            "instances_tested": len(diophantine_counts),
            "n_max": max_n,
            "conjecture_holds": correlation >= 0.8,
            "counterexample": "" if correlation >= 0.8 else f"correlation={correlation:.2f}"
        }
    
    return main()

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f} n_max={max(r['n_max'] for r in results)}")