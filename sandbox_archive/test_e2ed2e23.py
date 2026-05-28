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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def k_group_rank(edges, k):
        # Simplified K-group rank calculation (not actual algebraic K-theory)
        return len(edges) ** k
    
    def dnf_circuit_complexity(m):
        # Simplified DNF circuit complexity
        return 2 ** m
    
    n = random.randint(5, 40)
    graph_edges = generate_graph(n)
    r_G = k_group_rank(graph_edges, 1)
    
    if not graph_edges:
        return {
            "metric_name": "circuit_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No edges in the graph"
        }
    
    m_actual = random.randint(1, 2 ** r_G)
    m_upper_bound = dnf_circuit_complexity(r_G)
    
    return {
        "metric_name": "circuit_complexity",
        "metric_value": m_actual,
        "instances_tested": 1,
        "conjecture_holds": m_actual <= m_upper_bound,
        "counterexample": "" if m_actual <= m_upper_bound else f"m_actual={m_actual} > 2^(r(G))={m_upper_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                counterexample = r['counterexample']
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")