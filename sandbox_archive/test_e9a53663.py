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
    
    def generate_tseitin_formula(n, d):
        # Generate a random d-regular graph with n vertices
        adjacency_list = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d - 1)
            while any(j in adjacency_list[i] for j in neighbors):
                neighbors = random.sample(range(n), d - 1)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
                    edges.add((i, j))
        
        # Generate Tseitin formula
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in adjacency_list[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        
        # Add clauses for edges
        for (i, j) in edges:
            clauses.append([f'-{literals[i]}', f'{literals[j]}'])
            clauses.append([f'-{literals[j]}', f'{literals[i]}'])
        
        return adjacency_list, literals, clauses
    
    def geometric_entropy(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph)
        entropy = 0
        for neighbors in graph:
            if neighbors:
                p = Fraction(len(neighbors), degree_sum)
                entropy -= p * math.log2(p)
        return entropy
    
    def resolution_width(clauses):
        # Simplified resolution width calculation
        max_width = 0
        for clause in clauses:
            max_width = max(max_width, len([x for x in clause if not x.startswith('-')]))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropy_values = []
    width_values = []
    
    for n in n_values:
        adjacency_list, literals, clauses = generate_tseitin_formula(n, d=3)
        entropy = geometric_entropy(adjacency_list)
        width = resolution_width(clauses)
        
        entropy_values.append(entropy)
        width_values.append(width)
    
    instances_tested = len(entropy_values)
    n_max = max(n_values)
    
    correlation_coefficient = (instances_tested * sum(e * w for e, w in zip(entropy_values, width_values)) -
                                sum(entropy_values) * sum(width_values)) / \
                               math.sqrt((instances_tested * sum(e**2 for e in entropy_values) - sum(entropy_values)**2) *
                                         (instances_tested * sum(w**2 for w in width_values) - sum(width_values)**2))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * instances_tested - 3)))
    
    conjecture_holds = correlation_coefficient >= 0.7 and p_value < 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> p_value=<{}>".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "Geometric Entropy vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))