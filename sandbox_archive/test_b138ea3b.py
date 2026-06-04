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
    
    def generate_circuit(n, m):
        return [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
    
    def is_monotone(circuit):
        n, m = len(circuit), len(circuit[0])
        if not all(row[i] == row[0][i] for row in circuit for i in range(m)):
            return False
        for j in range(1, n):
            if any(circuit[j][i] < circuit[j-1][i] for i in range(m)):
                return False
        return True
    
    def monotone_width(circuit):
        if not is_monotone(circuit):
            return 0
        n, m = len(circuit), len(circuit[0])
        width = 0
        for j in range(1, n):
            if all(circuit[j][i] == circuit[j-1][i] for i in range(m)):
                width += 1
            else:
                break
        return width
    
    def automorphism_group(graph):
        n = len(graph)
        group = []
        visited = [False] * n
        
        def dfs(node, path):
            if node == n:
                group.append(path[:])
                return
            for i in range(n):
                if not visited[i]:
                    visited[i] = True
                    path.append(i)
                    dfs(node + 1, path)
                    path.pop()
                    visited[i] = False
        
        dfs(0, [])
        return group
    
    def geometric_group_order(group):
        return len(group)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, n)
            if not is_monotone(circuit):
                continue
            order = geometric_group_order(automorphism_group(circuit))
            width = monotone_width(circuit)
            total_order += order
            total_width += width
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Geometric Group Order vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No monotone circuits generated"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip(range(1, instances_tested + 1), range(1, instances_tested + 1))) -
                               sum(range(1, instances_tested + 1)) * mean_order * mean_width) / math.sqrt(
        (instances_tested * sum(order ** 2 for order in range(1, instances_tested + 1)) - sum(range(1, instances_tested + 1)) ** 2) *
        (instances_tested * sum(width ** 2 for width in range(1, instances_tested + 1)) - sum(range(1, instances_tested + 1)) ** 2))
    
    return {
        "metric_name": "Geometric Group Order vs Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")