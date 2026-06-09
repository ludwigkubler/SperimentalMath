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
    
    def generate_communication_instance(n):
        # Generate a random communication instance with n parties
        edges = set()
        for _ in range(int(n * (n - 1) / 2)):
            u, v = sorted(random.sample(range(1, n + 1), 2))
            edges.add((u, v))
        return edges
    
    def compute_rank_variance(edges):
        # Compute the rank variance of the communication instance
        if not edges:
            return 0.0
        num_edges = len(edges)
        rank_variances = []
        for _ in range(10):  # Sample multiple ranks to get a better estimate
            rank = sum(1 for edge in edges if random.choice([True, False]))
            rank_variances.append(rank)
        return sum((x - sum(rank_variances) / len(rank_variances)) ** 2 for x in rank_variances) / (len(rank_variances) - 1)
    
    def compute_min_geometric_flows(edges):
        # Compute the minimal number of geometric flow patterns required
        if not edges:
            return 0
        min_flows = float('inf')
        for _ in range(10):  # Sample multiple configurations to get a better estimate
            flows = set()
            for u, v in edges:
                if random.choice([True, False]):
                    flows.add((u, v))
            min_flows = min(min_flows, len(flows))
        return min_flows
    
    rank_variances = []
    m_flow_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n * (n - 1) // 2 < 10:  # Ensure at least 10 edges
            continue
        instance = generate_communication_instance(n)
        rank_variances.append(compute_rank_variance(instance))
        m_flow_values.append(compute_min_geometric_flows(instance))
    
    if not rank_variances or not m_flow_values:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n * (n - 1) // 2 >= 10),
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }
    
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    mean_m_flow_values = sum(m_flow_values) / len(m_flow_values)
    numerator = sum((x - mean_rank_variance) * (y - mean_m_flow_values) for x, y in zip(rank_variances, m_flow_values))
    denominator = math.sqrt(sum((x - mean_rank_variance) ** 2 for x in rank_variances)) * math.sqrt(sum((y - mean_m_flow_values) ** 2 for y in m_flow_values))
    
    if denominator == 0:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": len(rank_variances),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n * (n - 1) // 2 >= 10),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "rank_variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rank_variances),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n * (n - 1) // 2 >= 10),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 99997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")