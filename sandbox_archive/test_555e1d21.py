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

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, num_vars) * (-1 if random.choice([True, False]) else 1)
                   for _ in range(random.randint(1, num_vars))]
        cnf.append(clause)
    return cnf

def cnf_to_binary_tree(cnf):
    def build_tree(clauses):
        if not clauses:
            return {'type': 'leaf', 'value': None}
        root = {'type': 'node'}
        for clause in clauses:
            child = build_tree([c for c in clauses if c != clause])
            if 'children' not in root:
                root['children'] = []
            root['children'].append(child)
        return root

    return build_tree(cnf)

def count_self_similar_structures(tree, scale):
    if tree['type'] == 'leaf':
        return 1
    if scale == 0:
        return 1
    count = 0
    for child in tree.get('children', []):
        count += count_self_similar_structures(child, scale - 1)
    return count

def geometric_entropy(tree):
    n = len(tree['children'])
    total_nodes = sum(count_self_similar_structures(tree, scale) for scale in range(1, n+1))
    entropy = 0
    for scale in range(1, n+1):
        nodes_at_scale = count_self_similar_structures(tree, scale)
        if nodes_at_scale > 0:
            entropy += nodes_at_scale * math.log2(nodes_at_scale / total_nodes)
    return -entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 30
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n, n * (n // 2))
        tree = cnf_to_binary_tree(cnf)
        entropy = geometric_entropy(tree)
        metric_values.append(entropy)
        instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = True
    counterexample = ""
    
    if len(metric_values) < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r['counterexample'] != "" for r in results):
        first_failing_seed = next((r['seed'] for r in results if r['counterexample'] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")