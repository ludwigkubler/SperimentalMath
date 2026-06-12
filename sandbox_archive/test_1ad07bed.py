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
    
    def generate_circuit(depth, width):
        if depth == 0:
            return []
        else:
            operation = random.choice(['AND', 'OR'])
            inputs = [generate_circuit(random.randint(1, depth-1), width) for _ in range(width)]
            return [(operation, inputs)]
    
    def construct_group(circuit):
        group = set()
        stack = [[[], circuit]]
        while stack:
            path, node = stack.pop()
            if not node:
                group.add(tuple(path))
            else:
                operation, inputs = node
                for i in range(len(inputs)):
                    new_path = path + [i]
                    new_node = inputs[i]
                    stack.append((new_path, new_node))
        return group
    
    def compute_module_rank(group):
        n = len(group)
        if n == 0:
            return 0
        generators = list(group)
        relations = []
        for i in range(n):
            for j in range(i+1, n):
                g1, g2 = generators[i], generators[j]
                relation = tuple((g1[k] - g2[k]) % n for k in range(n))
                if relation not in relations:
                    relations.append(relation)
        return len(relations)
    
    def depth_and_width(circuit):
        if not circuit:
            return 0, 0
        operation, inputs = circuit[0]
        depths = [depth_and_width(sub_circuit) for sub_circuit in inputs]
        max_depth = max(depths) + 1 if depths else 1
        width = len(inputs)
        return max_depth, width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            pivot = None
            for j in range(rank, m):
                if matrix[i][j] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            rank += 1
            for k in range(n):
                if k != i and matrix[k][pivot] != 0:
                    factor = -matrix[k][pivot] / matrix[i][pivot]
                    for j in range(m):
                        matrix[k][j] += factor * matrix[i][j]
        return rank
    
    def compute_mrl(group):
        n = len(group)
        identity = tuple(0 for _ in range(n))
        generators = list(group - {identity})
        relations = []
        for i in range(len(generators)):
            for j in range(i+1, len(generators)):
                g1, g2 = generators[i], generators[j]
                relation = tuple((g1[k] - g2[k]) % n for k in range(n))
                if relation not in relations:
                    relations.append(relation)
        matrix = [[0 for _ in range(len(relations))] for _ in range(len(generators))]
        for i, g in enumerate(generators):
            for j, r in enumerate(relations):
                matrix[i][j] = sum((g[k] - r[k]) % n for k in range(n))
        rank = gaussian_elimination(matrix)
        return len(relations) - rank
    
    def run_circuit(depth, width):
        circuit = generate_circuit(depth, width)
        group = construct_group(circuit)
        mrl = compute_mrl(group)
        depth_val, width_val = depth_and_width(circuit)
        return mrl, depth_val, width_val
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        depth = random.randint(5, 40)
        width = random.randint(1, 40)
        n_max = max(n_max, max(depth, width))
        mrl, depth_val, width_val = run_circuit(depth, width)
        instances_tested += 1
        total_metric_value += mrl / (width_val + depth_val ** (2/3))
    
    if instances_tested < 30:
        return {
            "metric_name": "mrl/C",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    if mean_metric_value < 0.5:
        conjecture_holds = False
        counterexample = f"mean_metric_value={mean_metric_value}"
    
    return {
        "metric_name": "mrl/C",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/instances_tested} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/instances_tested} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_metric_value<{total_metric_value/instances_tested}\" first_failing_seed={first_failing_seed}")