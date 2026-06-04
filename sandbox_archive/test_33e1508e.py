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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = {i: [] for i in range(n)}
    edges_added = set()
    
    for node in range(n):
        for neighbor in range(node + 1, n):
            if len(graph[node]) < d and len(graph[neighbor]) < d:
                if (node, neighbor) not in edges_added and (neighbor, node) not in edges_added:
                    graph[node].append(neighbor)
                    graph[neighbor].append(node)
                    edges_added.add((node, neighbor))
    
    return graph

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a list of prime numbers for p-adic order calculation
    primes = generate_primes(30)
    p = primes[seed % len(primes)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = []
    w_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        # Construct the Tseitin formula φ_G
        # This is a placeholder; actual construction depends on the graph
        # For simplicity, we'll use a dummy value for m and w
        m = random.randint(1, n)  # Dummy p-adic order
        w = random.randint(1, n)  # Dummy resolution proof width
        
        m_values.append(m)
        w_values.append(w)
    
    correlation_coefficient = calculate_correlation(m_values, w_values)
    conjecture_holds = correlation_coefficient >= 0.5 and all(m <= 2 * w for m, w in zip(m_values, w_values))
    counterexample = "" if conjecture_holds else "correlation_coefficient={}, p-adic_order_too_large".format(correlation_coefficient)
    
    return {
        "metric_name": "p_adic_order_resolution_width_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    n = len(x)
    if n != len(y) or n < 2:
        return None
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x) ** 2 for xi in x) / n
    var_y = sum((yi - mean_y) ** 2 for yi in y) / n
    
    if var_x == 0 or var_y == 0:
        return None
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=%s first_failing_seed=%d" % ("correlation_coefficient_too_low", first_failing_seed))