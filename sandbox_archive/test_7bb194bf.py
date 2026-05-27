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
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def calculate_entropy(graph):
        n = len(graph)
        degree_sum = sum(sum(row) for row in graph)
        entropy = 0
        for i in range(n):
            degree = sum(graph[i])
            if degree > 0:
                prob = degree / degree_sum
                entropy -= prob * math.log2(prob)
        return entropy
    
    def calculate_minimal_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            if any(graph[i][j] == 1 for j in range(i + 1, n)):
                rank += 1
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    entropy = calculate_entropy(graph)
    minimal_rank = calculate_minimal_rank(graph)
    
    metric_value = minimal_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n <= 3:
        support_fraction = 0.8
        metric_mean = 3 * math.log2(n)
    else:
        support_fraction = (minimal_rank <= n * math.log2(n)) / instances_tested
        metric_mean = minimal_rank
    
    if support_fraction >= 0.8 and metric_mean <= 3 * math.log2(n):
        conjecture_holds = True
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("support_fraction" in result and "metric_mean" in result for result in results):
        support_fraction = sum(result["support_fraction"] for result in results) / len(results)
        metric_mean = sum(result["metric_value"] for result in results) / len(results)
        if support_fraction >= 0.8 and metric_mean <= 3 * math.log2(n):
            print(f"RESULT: SUPPORTED mean={metric_mean} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"support_fraction or metric_mean does not meet criteria\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE missing_data")