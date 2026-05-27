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
    
    def generate_random_graph(n):
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
    def graph_entropy(adj_matrix):
        n = len(adj_matrix)
        degree_sum = sum(sum(row) for row in adj_matrix)
        if degree_sum == 0:
            return 0
        avg_degree = degree_sum / (n * (n - 1))
        entropy = -avg_degree * math.log2(avg_degree) - (1 - avg_degree) * math.log2(1 - avg_degree)
        return entropy
    
    def monomial_ideal_rank(adj_matrix):
        n = len(adj_matrix)
        rank = 0
        for i in range(n):
            if sum(adj_matrix[i]) > 0:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    adj_matrix = generate_random_graph(n)
    entropy = graph_entropy(adj_matrix)
    rank = monomial_ideal_rank(adj_matrix)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rank >= Fraction(2**n, math.exp(entropy)) and rank <= n * math.log(n):
        conjecture_holds = True
    
    return {
        "metric_name": "monomial_ideal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean_d)**2 for x in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8 and max(metric_values) <= 3 * math.log2(max(n for n, _ in [(r["instances_tested"], r["metric_value"]) for r in results])):
        mean_d = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean_d)**2 for x in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank_out_of_bounds\" first_failing_seed={first_failing_seed}")