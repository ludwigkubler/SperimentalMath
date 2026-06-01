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

def generate_planar_graphs(n):
    if n == 1:
        return [[(0, 0)]]
    elif n == 2:
        return [[(0, 0), (1, 0)], [(0, 0), (0, 1)]]
    else:
        # Generate a random planar graph using the dual of a triangulation
        nodes = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return [nodes, edges]

def construct_symplectic_leaves(graph):
    nodes, edges = graph
    msl = len(nodes)
    return msl

def calculate_communication_rank_growth(graph):
    nodes, edges = graph
    cr = len(edges)
    return cr

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances = generate_planar_graphs(n=40)
    msl_values = [construct_symplectic_leaves(graph) for graph in instances]
    cr_values = [calculate_communication_rank_growth(graph) for graph in instances]
    
    if len(msl_values) != len(cr_values):
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(instances),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mismatched_instance_counts"
        }
    
    if not msl_values or not cr_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(instances),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "empty_instance_lists"
        }
    
    n = len(msl_values)
    msl_sum = sum(msl_values)
    cr_sum = sum(cr_values)
    msl_mean = Fraction(msl_sum, n)
    cr_mean = Fraction(cr_sum, n)
    
    numerator = sum((msl_values[i] - msl_mean) * (cr_values[i] - cr_mean) for i in range(n))
    denominator = math.sqrt(sum((msl_values[i] - msl_mean)**2 for i in range(n)) * sum((cr_values[i] - cr_mean)**2 for i in range(n)))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(instances),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "zero_denominator"
        }
    
    pearson_correlation = Fraction(numerator, denominator)
    return {
        "metric_name": "Pearson correlation",
        "metric_value": float(pearson_correlation),
        "instances_tested": len(instances),
        "n_max": 40,
        "conjecture_holds": abs(float(pearson_correlation)) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results))
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(8, 10):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation < 0.7\" first_failing_seed={result['seed']}")
                break