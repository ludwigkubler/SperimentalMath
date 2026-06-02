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
    
    def generate_d_regular_circuit(n, d):
        if n < 1 or d < 1 or d >= n:
            return None
        circuit = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                circuit[u][v] = 1
                circuit[v][u] = 1
                edges.add((u, v))
        return circuit
    
    def compute_p_adic_hodge_rank(circuit):
        n = len(circuit)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if circuit[i][j] == 1:
                    A[i][j] = 1
        rank = 0
        for row in A:
            if any(row):
                rank += 1
                for j in range(n):
                    if row[j]:
                        for k in range(n):
                            A[k][j] -= row[k]
        return rank
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j)) != 0]
            if all(circuit[u][v] == 0 for u in subset for v in subset if u != v):
                width = max(width, len(subset))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_d_regular_circuit(n, d=3)
        if circuit is None:
            continue
        min_rank = compute_p_adic_hodge_rank(circuit)
        w_C = compute_monotone_width(circuit)
        results.append((min_rank, w_C))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_ranks = [r[0] for r in results]
    w_Cs = [r[1] for r in results]
    n_max = max(n_values)
    instances_tested = len(results)
    
    # Calculate Pearson correlation coefficient
    mean_min_rank = sum(min_ranks) / instances_tested
    mean_w_C = sum(w_Cs) / instances_tested
    numerator = sum((min_ranks[i] - mean_min_rank) * (w_Cs[i] - mean_w_C) for i in range(instances_tested))
    denominator = math.sqrt(sum((min_ranks[i] - mean_min_rank) ** 2 for i in range(instances_tested))) * \
                  math.sqrt(sum((w_Cs[i] - mean_w_C) ** 2 for i in range(instances_tested)))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")