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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def min_cut_capacity(graph, source, sink):
        n = len(graph)
        visited = [False] * n
        parent = [-1] * n
        
        def bfs():
            queue = [source]
            visited[source] = True
            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if not visited[v] and graph[u][v] > 0:
                        queue.append(v)
                        parent[v] = u
                        visited[v] = True
            return visited[sink]
        
        max_flow = 0
        while bfs():
            path_flow = float('Inf')
            s = sink
            
            while s != source:
                path_flow = min(path_flow, graph[parent[s]][s])
                s = parent[s]
            
            v = sink
            while v != source:
                u = parent[v]
                graph[u][v] -= path_flow
                graph[v][u] += path_flow
                v = parent[v]
            
            max_flow += path_flow
        
        return max_flow
    
    def calculate_entropy(probabilities):
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        graph = [[0] * (2**n) for _ in range(2**n)]
        
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    graph[i][j] = 1
        
        source, sink = 0, 2**n - 1
        communication_complexity = min_cut_capacity(graph, source, sink)
        
        probabilities = [f.count(1) / len(f), f.count(0) / len(f)]
        entropy = calculate_entropy(probabilities)
        
        metric_values.append({"metric_name": "communication_complexity", "metric_value": communication_complexity})
        metric_values.append({"metric_name": "entropy", "metric_value": entropy})
    
    mean_communication_complexity = sum(x["metric_value"] for x in metric_values if x["metric_name"] == "communication_complexity") / len(metric_values)
    mean_entropy = sum(x["metric_value"] for x in metric_values if x["metric_name"] == "entropy") / len(metric_values)
    
    correlation_coefficient = 0.0
    n_max = max(n_values)
    instances_tested = len(metric_values)
    
    for i in range(instances_tested):
        communication_complexity = metric_values[i]["metric_value"]
        entropy = metric_values[instances_tested + i]["metric_value"]
        correlation_coefficient += (communication_complexity - mean_communication_complexity) * (entropy - mean_entropy)
    
    correlation_coefficient /= instances_tested * math.sqrt((sum((x["metric_value"] - mean_communication_complexity)**2 for x in metric_values if x["metric_name"] == "communication_complexity") / instances_tested) * 
                                                           (sum((x["metric_value"] - mean_entropy)**2 for x in metric_values if x["metric_name"] == "entropy") / instances_tested))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")