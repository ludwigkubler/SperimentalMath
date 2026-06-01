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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i+1}" for i in range(n)]
        clauses = []
        for i in range(n):
            clause = []
            for j in graph[i]:
                if j < i:
                    continue
                clause.append(f"~{literals[j]}")
            clauses.append(" | ".join(clause))
        for i in range(n):
            clauses.append(f"{literals[i]} | {' | '.join([f'~{literals[j]}' for j in graph[i]])}")
        return " & ".join(clauses)
    
    def resolution_width(formula):
        # Simplified DPLL solver to estimate width
        stack = []
        literals = set()
        for clause in formula.split(" & "):
            if " | " not in clause:
                continue
            literals.update(clause.split(" | "))
            stack.append(clause)
        
        def simplify(stack, literals):
            while stack:
                clause = stack.pop()
                if " | " not in clause:
                    continue
                pos_lit = next((l for l in literals if l in clause), None)
                neg_lit = next((f"~{l}" for l in literals if f"~{l}" in clause), None)
                if pos_lit and neg_lit:
                    stack.remove(pos_lit)
                    stack.remove(neg_lit)
                    literals.discard(pos_lit)
                    literals.discard(neg_lit)
                else:
                    return len(literals)
            return 0
        
        width = simplify(stack, literals)
        return width
    
    def quotient_sheaves(graph):
        n = len(graph)
        sheaves = [set() for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                if j < i:
                    continue
                sheaves[i].add(j)
                sheaves[j].add(i)
        return sheaves
    
    def min_index(sheaves):
        n = len(sheaves)
        max_index = 0
        for i in range(n):
            index = sum(1 for j in sheaves[i] if len(sheaves[j]) > len(sheaves[i]))
            max_index = max(max_index, index)
        return max_index
    
    d_values = [3, 4, 5, 6, 7, 8]
    results = []
    
    for d in d_values:
        n = random.randint(10, 20)  # Ensure n is at least 5 and n_max >= 20
        graph = generate_d_regular_graph(d, n)
        if not graph:
            continue
        
        formula = tseitin_formula(graph)
        width = resolution_width(formula)
        sheaves = quotient_sheaves(graph)
        index = min_index(sheaves)
        
        results.append({
            "n": n,
            "d": d,
            "width": width,
            "index": index
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    correlation_values = [result["width"] * result["index"] for result in results]
    mean_correlation = sum(correlation_values) / instances_tested
    std_deviation = math.sqrt(sum((x - mean_correlation) ** 2 for x in correlation_values) / instances_tested)
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.3 <= corr >= 0.7 for corr in correlation_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.7\" first_failing_seed={r['seed']}")
                break