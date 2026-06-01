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
    
    def generate_k_colorable_graph(n, k):
        if n <= 1 or k < 2:
            return None
        
        graph = {i: [] for i in range(n)}
        
        colors = list(range(k))
        color_assignment = [random.choice(colors) for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                if color_assignment[i] != color_assignment[j]:
                    graph[i].append(j)
                    graph[j].append(i)
        
        return graph
    
    def hasse_weil_l_function(graph):
        n = len(graph)
        lrank = 0
        
        for i in range(n):
            neighbors = graph[i]
            if not neighbors:
                continue
            
            degree = len(neighbors)
            lrank += math.log(degree + 1, 2)
        
        return lrank
    
    def communication_rank_growth_rate(graph):
        n = len(graph)
        crg_rate = 0
        
        for i in range(n):
            neighbors = graph[i]
            if not neighbors:
                continue
            
            degree = len(neighbors)
            crg_rate += degree / (n - 1)
        
        return crg_rate
    
    def pearson_correlation(lrank_values, crg_rate_values):
        n = len(lrank_values)
        mean_lrank = sum(lrank_values) / n
        mean_crg_rate = sum(crg_rate_values) / n
        
        numerator = sum((lrank_values[i] - mean_lrank) * (crg_rate_values[i] - mean_crg_rate) for i in range(n))
        denominator = math.sqrt(sum((lrank_values[i] - mean_lrank) ** 2 for i in range(n))) * math.sqrt(sum((crg_rate_values[i] - mean_crg_rate) ** 2 for i in range(n)))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    n_max = 40
    instances_tested = 30
    lrank_values = []
    crg_rate_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        k = random.randint(2, min(n, 10))
        
        graph = generate_k_colorable_graph(n, k)
        if not graph:
            continue
        
        lrank = hasse_weil_l_function(graph)
        crg_rate = communication_rank_growth_rate(graph)
        
        lrank_values.append(lrank)
        crg_rate_values.append(crg_rate)
    
    if not lrank_values or not crg_rate_values:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty graph or no valid graphs generated"
        }
    
    correlation = pearson_correlation(lrank_values, crg_rate_values)
    mean_lrank = sum(lrank_values) / len(lrank_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and mean_lrank <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_lrank <= 3 else f"correlation < 0.8 or mean lrank > 3"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")