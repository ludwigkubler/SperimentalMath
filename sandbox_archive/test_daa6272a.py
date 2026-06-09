# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def cayley_graph(instance):
        n = len(instance)
        graph = defaultdict(set)
        for x in range(n):
            for y in instance:
                if (x + y) % n not in graph[x]:
                    graph[x].add((x + y) % n)
        return graph
    
    def max_order(graph, n):
        orders = [0] * n
        visited = [False] * n
        queue = []
        
        for start in range(n):
            if not visited[start]:
                queue.append(start)
                while queue:
                    current = queue.pop(0)
                    if not visited[current]:
                        visited[current] = True
                        orders[start] += 1
                        for neighbor in graph[current]:
                            if not visited[neighbor]:
                                queue.append(neighbor)
        
        return max(orders)
    
    def communication_complexity(instance):
        # Placeholder function, replace with actual implementation
        return len(instance)  # Example: complexity is proportional to the length of the instance
    
    n_values = [5, 10, 15, 20, 30, 40]
    g_sum = 0
    o_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = [random.randint(1, n-1) for _ in range(n)]
            graph = cayley_graph(instance)
            g_value = len(graph)
            o_value = max_order(graph, n)
            r_value = communication_complexity(instance)
            
            g_sum += g_value
            o_sum += o_value
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_g = Fraction(g_sum, instances_tested)
    mean_o = Fraction(o_sum, instances_tested)
    correlation_coefficient = (instances_tested * sum(g * r for g, r in zip([g_value for _ in range(instances_tested)], [r_value for _ in range(instances_tested)])) - g_sum * o_sum) / (math.sqrt(instances_tested * sum((g - mean_g)**2 for g in [g_value for _ in range(instances_tested)]) * instances_tested * sum((o - mean_o)**2 for o in [o_value for _ in range(instances_tested)])))
    
    conjecture_holds = correlation_coefficient >= Fraction(7, 10) and abs(mean_o - mean_g) <= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")