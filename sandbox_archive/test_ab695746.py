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

def generate_random_instance(d, n=30):
    graph = {}
    for i in range(n):
        neighbors = random.sample(range(n), d)
        while len(neighbors) != len(set(neighbors)):
            neighbors = random.sample(range(n), d)
        graph[i] = {neighbor: random.randint(1, 10) for neighbor in neighbors}
    
    cnf = []
    for i in range(n):
        for j in range(i + 1, n):
            if not any(graph[i][k] == graph[j][k] for k in range(d)):
                literals = [i * d + k + 1 for k in range(d)] + [-((j - i) * d + k + 1) for k in range(d)]
                cnf.append(literals)
    
    lattice_point_count = count_lattice_points(graph, d)
    return cnf, lattice_point_count

def count_lattice_points(graph, d):
    n = len(graph)
    min_dist = float('inf')
    for point in itertools.product(range(1, 2), repeat=d):
        dist = sum(abs(point[k] - graph[i][k]) for i in range(n) for k in range(d))
        if dist < min_dist:
            min_dist = dist
    return min_dist

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d_values = [5, 10, 15, 20, 30, 40]
    lattice_point_counts = []
    clause_set_sizes = []
    
    for d in d_values:
        cnf, lattice_point_count = generate_random_instance(d)
        lattice_point_counts.append(lattice_point_count)
        clause_set_sizes.append(len(cnf))
    
    mean_lattice_point_count = sum(lattice_point_counts) / len(lattice_point_counts)
    mean_clause_set_size = sum(clause_set_sizes) / len(clause_set_sizes)
    
    correlation_coefficient = calculate_correlation(lattice_point_counts, clause_set_sizes)
    p_value = calculate_p_value(lattice_point_counts, clause_set_sizes, correlation_coefficient)
    
    conjecture_holds = correlation_coefficient > 0.8 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> p_value=<{}>".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(lattice_point_counts),
        "n_max": max(d_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    return numerator / denominator

def calculate_p_value(x, y, r):
    n = len(x)
    t_statistic = r * math.sqrt((n - 2) / (1 - r ** 2))
    degrees_of_freedom = n - 2
    p_value = 2 * (1 - scipy.stats.t.cdf(abs(t_statistic), degrees_of_freedom))
    return p_value

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(r["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")