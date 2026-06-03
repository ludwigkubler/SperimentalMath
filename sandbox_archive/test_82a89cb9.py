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
    
    def generate_communication_problem(r):
        # Generate a communication complexity problem with rank r
        # This is a placeholder function; replace it with actual implementation
        return [random.randint(1, 10) for _ in range(r)]
    
    def construct_cayley_graph(problem):
        # Construct the Cayley graph from the communication problem
        # This is a placeholder function; replace it with actual implementation
        n = len(problem)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(problem[i] - problem[j]) == 1:
                    G[i][j] = G[j][i] = 1
        return G
    
    def min_alexander_brinckmann_index(G):
        # Calculate the minimal Alexander-Brinckmann index of the Cayley graph
        n = len(G)
        if n <= 1:
            return 0
        
        # Placeholder for actual calculation; replace with actual implementation
        return sum(sum(row) for row in G) / (n * (n - 1))
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    def max_value(x):
        return max(x)
    
    instances_tested = 0
    n_max = 0
    total_r = 0
    total_A_Cayley = 0
    
    for r in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        problem = generate_communication_problem(r)
        G = construct_cayley_graph(problem)
        A_Cayley = min_alexander_brinckmann_index(G)
        
        total_r += r
        total_A_Cayley += A_Cayley
        instances_tested += 1
        n_max = max(n_max, len(G))
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient data"
        }
    
    mean_r = total_r / instances_tested
    mean_A_Cayley = total_A_Cayley / instances_tested
    
    corr = correlation([r for _ in range(instances_tested)], [A_Cayley for _ in range(instances_tested)])
    max_A_Cayley = max_value([A_Cayley for _ in range(instances_tested)])
    
    if corr >= 0.9 and max_A_Cayley <= 10 * mean_r ** 2:
        return {
            "metric_name": "Correlation",
            "metric_value": corr,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Correlation",
            "metric_value": corr,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Failed correlation: {corr}, max A_Cayley: {max_A_Cayley}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Failed correlation\" first_failing_seed={first_failing_seed}")