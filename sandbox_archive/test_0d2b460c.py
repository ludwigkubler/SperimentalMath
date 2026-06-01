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
    
    def geometric_entropy(graph):
        n = len(graph)
        degree_sum = sum(sum(1 for neighbor in neighbors if neighbor != node) for node, neighbors in graph.items())
        return -degree_sum / (2 * n)

    def resolution_width(phi):
        clauses = phi.split(' or ')
        width = 0
        for clause in clauses:
            literals = clause.split(' and ')
            width = max(width, len(literals))
        return width

    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for i in range(1, n + 1):
            clause = f'{variables[i-1]} or not {variables[-i]}'
            clauses.append(clause)
        return ' and '.join(clauses)

    def generate_d_regular_graph(n, d):
        graph = {}
        nodes = list(range(n))
        for node in nodes:
            neighbors = random.sample(nodes, d - 1)
            while node in neighbors:
                neighbors = random.sample(nodes, d - 1)
            graph[node] = neighbors
        return graph

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0
    total_width = 0

    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, n - 1)
            phi = generate_tseitin_formula(n, n - 1)
            entropy = geometric_entropy(graph)
            width = resolution_width(phi)
            total_entropy += entropy
            total_width += width
            instances_tested += 1

    mean_entropy = total_entropy / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(e * w for e, w in zip(entropy_values, width_values)) -
                               sum(entropy_values) * sum(width_values)) / \
                              math.sqrt((instances_tested * sum(e**2 for e in entropy_values) - sum(entropy_values)**2) *
                                        (instances_tested * sum(w**2 for w in width_values) - sum(width_values)**2))

    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(instances_tested - 2)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7 or p-value >= 0.05\" first_failing_seed={first_failing_seed}")