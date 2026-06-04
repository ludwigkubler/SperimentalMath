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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clauses.append([literals[u]])
            for v in graph[u]:
                clauses.append([-literals[u], literals[v]])
        return clauses
    
    def p_adic_order(monomial, p):
        if monomial == 0:
            return float('inf')
        order = 0
        while monomial % p == 0:
            monomial //= p
            order += 1
        return order
    
    def puiseux_series_expansion(f, x, p):
        series = [f(x)]
        for i in range(1, 10):  # Limit to first few terms for simplicity
            series.append(series[-1] * (x - f(x)) / i)
        return series
    
    def resolution_width(clauses):
        queue = clauses[:]
        while queue:
            clause = random.choice(queue)
            if len(clause) == 1:
                return len(queue)
            literal = random.choice(clause)
            new_clauses = []
            for c in queue:
                if literal not in c and -literal not in c:
                    new_clauses.append(c)
                elif -literal in c:
                    new_clauses.extend([c + [l] for l in clause if l != -literal])
            queue = new_clauses
        return len(queue)
    
    def is_p_adic_unit(coeff, p):
        return coeff % p == 1
    
    n_max = 40
    instances_tested = 0
    m_values = []
    w_values = []
    
    for n in range(5, n_max + 1, 5):
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        
        clauses = tseitin_formula(graph)
        w = resolution_width(clauses)
        
        m = float('inf')
        for x in range(-10, 11):  # Limit to a small range for simplicity
            series = puiseux_series_expansion(lambda y: sum([c[y] for c in clauses]), x, 2)
            for coeff in series:
                if is_p_adic_unit(coeff, 2):
                    m = min(m, p_adic_order(coeff, 2))
        
        if m == float('inf'):
            continue
        
        m_values.append(m)
        w_values.append(w)
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "p-adic order vs resolution width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = sum((m - mean_m) * (w - mean_w) for m, w in zip(m_values, w_values)) / math.sqrt(sum((m - mean_m)**2 for m in m_values) * sum((w - mean_w)**2 for w in w_values))
    max_m_over_w = max(m / w for m, w in zip(m_values, w_values))
    
    return {
        "metric_name": "p-adic order vs resolution width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5 and max_m_over_w <= 2,
        "counterexample": "" if correlation_coefficient >= 0.5 and max_m_over_w <= 2 else f"correlation_coefficient={correlation_coefficient} max_m_over_w={max_m_over_w}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")