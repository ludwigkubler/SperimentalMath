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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit != -other_lit for lit, other_lit in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def resolution_tree(cnf):
        tree = {}
        for clause in cnf:
            tree[tuple(sorted(clause))] = []
        for i in range(len(cnf)):
            for j in range(i + 1, len(cnf)):
                if any(lit == -other_lit for lit, other_lit in zip(cnf[i], cnf[j])):
                    new_clause = sorted(set(lit for lit in cnf[i] + cnf[j] if lit != -other_lit))
                    tree[tuple(sorted(new_clause))].append((i, j))
        return tree
    
    def euler_characteristic(tree):
        nodes = set()
        edges = set()
        for node, children in tree.items():
            nodes.add(node)
            for child in children:
                edges.add(tuple(sorted([node] + list(child))))
        return len(nodes) - len(edges)
    
    def width(tree):
        if not tree:
            return 0
        max_width = 0
        for node, children in tree.items():
            widths = [width(child_tree) for child_tree in children]
            if widths:
                max_width = max(max_width, max(widths) + 1)
        return max_width
    
    n_max = 5
    metric_values = []
    
    for n in range(5, 31):
        cnf = generate_cnf(n)
        tree = resolution_tree(cnf)
        chi = euler_characteristic(tree)
        w = width(tree)
        if w > 0:
            metric_values.append(chi / w)
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "chi_over_w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "chi_over_w",
        "metric_value": mean,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": mean >= 0.8 and std_dev <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={next(r['seed'] for r in results if not r['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")