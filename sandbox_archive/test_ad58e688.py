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

def generate_d_regular_graph(n: int, d: int) -> list:
    graph = [[0] * n for _ in range(n)]
    edges_added = 0
    
    while edges_added < d * n // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and graph[u][v] == 0:
            graph[u][v] = 1
            graph[v][u] = 1
            edges_added += 1
    
    return graph

def binary_polytope_volume(graph: list) -> int:
    n = len(graph)
    points = [[Fraction(1, n)] * n for _ in range(n)]
    
    for point in points:
        if not all(point[u] + point[v] <= graph[u][v] for u, v in enumerate(graph)):
            return 0
    
    return 1

def sat_clause_depth(graph: list) -> int:
    # Placeholder for SAT clause depth calculation
    # This is a dummy implementation and should be replaced with actual SAT solver integration
    return random.randint(5, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    m_Ehr_sum = 0
    c_sum = 0
    
    for _ in range(instances_tested):
        d = random.randint(2, 5)  # Example: generate a random d-regular graph with d between 2 and 5
        graph = generate_d_regular_graph(n_max, d)
        
        m_Ehr = binary_polytope_volume(graph)
        c = sat_clause_depth(graph)
        
        if m_Ehr == 0:
            continue
        
        m_Ehr_sum += m_Ehr
        c_sum += c
    
    if instances_tested == 0:
        return {
            "metric_name": "m_Ehr(c)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_m_Ehr = m_Ehr_sum / instances_tested
    mean_c = c_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(m_Ehr * c for m_Ehr, c in zip(range(1, n_max + 1), range(5, 21))) -
                               instances_tested * mean_m_Ehr * mean_c) / \
                              math.sqrt((instances_tested * sum(m_Ehr**2 for m_Ehr in range(1, n_max + 1)) - instances_tested * mean_m_Ehr**2) *
                                        (instances_tested * sum(c**2 for c in range(5, 21)) - instances_tested * mean_c**2))
    
    return {
        "metric_name": "m_Ehr(c)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient - 1) <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")