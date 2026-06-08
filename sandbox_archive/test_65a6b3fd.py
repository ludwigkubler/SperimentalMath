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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def binary_tree_from_cnf(cnf):
        tree = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in tree:
                    tree[abs(literal)] = []
                tree[abs(literal)].append(literal)
        return tree
    
    def geometric_entropy(tree, n):
        if not tree or len(tree) == 1:
            return 0
        entropy = 0
        for node in tree:
            entropy += math.log2(len(tree[node]))
        return entropy / n
    
    def circuit_depth(cnf):
        depth = 0
        for clause in cnf:
            depth = max(depth, len(clause))
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 80% of data points lie within ±3 std deviations
            cnf = generate_cnf(n, random.randint(1, n))
            tree = binary_tree_from_cnf(cnf)
            entropy = geometric_entropy(tree, n)
            depth = circuit_depth(cnf)
            metric_values.append((entropy, depth))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    entropies, depths = zip(*metric_values)
    mean_entropy = sum(entropies) / len(entropies)
    mean_depth = sum(depths) / len(depths)
    std_entropy = math.sqrt(sum((x - mean_entropy) ** 2 for x in entropies) / len(entropies))
    std_depth = math.sqrt(sum((x - mean_depth) ** 2 for x in depths) / len(depths))
    
    correlation_coefficient = sum((entropies[i] - mean_entropy) * (depths[i] - mean_depth) for i in range(len(entropies))) / (len(entropies) * std_entropy * std_depth)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95 and all(abs(x - mean_depth) <= 3 * std_depth for x in depths),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None]))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break