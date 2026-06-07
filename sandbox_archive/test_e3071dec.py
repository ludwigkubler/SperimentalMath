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
        if (n * d) % 2 != 0 or d > n - 1:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < d * n // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and graph[u][v] == 0:
                graph[u][v] = 1
                graph[v][u] = 1
                edges_added += 1
        return graph
    
    def binary_polytope_volume(graph):
        n = len(graph)
        volume = 0
        for i in range(2**n):
            point = [i >> j & 1 for j in range(n)]
            if all(point[u] + point[v] <= graph[u][v] for u, v in enumerate(graph)):
                volume += 1
        return volume
    
    def sat_clause_depth(graph):
        # Placeholder for SAT solver
        # This is a dummy implementation and should be replaced with an actual SAT solver
        return random.randint(5, 20)
    
    n_max = 40
    instances_tested = 0
    m_Ehr_values = []
    c_G_values = []
    
    for n in range(5, n_max + 1):
        d = random.randint(2, min(n-1, 3))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        instances_tested += 1
        m_Ehr = binary_polytope_volume(graph)
        c_G = sat_clause_depth(graph)
        
        m_Ehr_values.append(m_Ehr)
        c_G_values.append(c_G)
    
    if not m_Ehr_values or not c_G_values:
        return {
            "metric_name": "m_Ehr vs c(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_m_Ehr = sum(m_Ehr_values) / len(m_Ehr_values)
    mean_c_G = sum(c_G_values) / len(c_G_values)
    correlation_coefficient = 0
    
    for m, c in zip(m_Ehr_values, c_G_values):
        correlation_coefficient += (m - mean_m_Ehr) * (c - mean_c_G)
    
    correlation_coefficient /= math.sqrt(sum((m - mean_m_Ehr)**2 for m in m_Ehr_values)) * math.sqrt(sum((c - mean_c_G)**2 for c in c_G_values))
    
    return {
        "metric_name": "m_Ehr vs c(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.99,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) >= 0.99 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'] and abs(result['metric_value']) >= 0.99)}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")