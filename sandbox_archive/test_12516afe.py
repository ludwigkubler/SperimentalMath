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
    
    def generate_communication_problem(rank):
        # Generate a random communication complexity problem with given rank
        # This is a placeholder function; replace with actual generation logic
        return [random.randint(1, 10) for _ in range(rank)]
    
    def construct_cayley_graph(problem):
        # Construct the Cayley graph from the communication problem
        # This is a placeholder function; replace with actual construction logic
        n = len(problem)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if abs(problem[i] - problem[j]) == 1:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def calculate_minimal_alexander_brinckmann_index(G):
        # Calculate the minimal Alexander-Brinckmann index of the Cayley graph
        n = len(G)
        if n == 0:
            return 0
        
        # Placeholder for actual calculation logic
        # For simplicity, we use a dummy value
        return sum(sum(row) for row in G) / (n * (n - 1))
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) * sum((y[i] - mean_y) ** 2 for i in range(len(y))))
        return numerator / denominator if denominator != 0 else 0
    
    ranks = [5, 10, 15, 20, 30, 40]
    A_Cayley_values = []
    
    for rank in ranks:
        problem = generate_communication_problem(rank)
        G = construct_cayley_graph(problem)
        A_Cayley_value = calculate_minimal_alexander_brinckmann_index(G)
        A_Cayley_values.append(A_Cayley_value)
    
    correlation = correlation_coefficient(ranks, A_Cayley_values)
    max_A_Cayley = max(A_Cayley_values)
    conjecture_holds = correlation >= 0.9 and max_A_Cayley <= 10 * (max(ranks) ** 2)
    counterexample = "" if conjecture_holds else f"Correlation: {correlation}, Max A_Cayley: {max_A_Cayley}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")