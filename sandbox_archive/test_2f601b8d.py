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
    
    def generate_bipartite_graph(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n // 2):
            for j in range(n // 2, n):
                if random.random() < 0.5:
                    A[i][j] = 1
        return A
    
    def frobenius_representation_count(A):
        n = len(A)
        count = set()
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j]:
                    count.add((i, j))
        return len(count)
    
    def communication_complexity_rank_variance(A):
        n = len(A)
        rank = 0
        for i in range(n):
            row = [A[i][j] for j in range(n)]
            if any(row):
                rank += 1
        return (rank - 1) ** 2
    
    def mean(values):
        return sum(values) / len(values)
    
    def std_dev(values, mean):
        return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
    
    n_values = [5, 10, 15, 20, 30, 40]
    frobenius_counts = []
    comm_rank_vars = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = generate_bipartite_graph(n)
            frobenius_counts.append(frobenius_representation_count(A))
            comm_rank_vars.append(communication_complexity_rank_variance(A))
    
    mean_frobenius = mean(frobenius_counts)
    std_dev_frobenius = std_dev(frobenius_counts, mean_frobenius)
    mean_comm_rank_var = mean(comm_rank_vars)
    std_dev_comm_rank_var = std_dev(comm_rank_vars, mean_comm_rank_var)
    
    correlation_coefficient = (sum((frobenius_counts[i] - mean_frobenius) * (comm_rank_vars[i] - mean_comm_rank_var) for i in range(len(frobenius_counts))) / len(frobenius_counts)) / (std_dev_frobenius * std_dev_comm_rank_var)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(frobenius_counts),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = std_dev([r["metric_value"] for r in results], mean_metric_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient < 0.95"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")