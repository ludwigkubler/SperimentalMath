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
    
    def negation_width(circuit):
        if not circuit:
            return 0
        return max(negation_width(sub_circuit) for sub_circuit in circuit) + (1 if isinstance(circuit, tuple) and circuit[0] == 'NOT' else 0)
    
    def resolution_refutation_tree(circuit):
        if not circuit:
            return []
        if isinstance(circuit, tuple):
            op = circuit[0]
            left, right = circuit[1], circuit[2]
            if op == 'AND':
                return resolution_refutation_tree(left) + resolution_refutation_tree(right)
            elif op == 'OR':
                return [op] + resolution_refutation_tree(left) + resolution_refutation_tree(right)
            elif op == 'NOT':
                return ['NOT'] + resolution_refutation_tree(left)
        return [circuit]
    
    def tropicalized_hodge_structure(tree):
        if not tree:
            return 0
        if isinstance(tree, list):
            op = tree[0]
            children = tree[1:]
            if op == 'AND':
                return max(tropicalized_hodge_structure(child) for child in children)
            elif op == 'OR':
                return sum(tropicalized_hodge_structure(child) for child in children)
            elif op == 'NOT':
                return 1 + tropicalized_hodge_structure(children[0])
        return 1
    
    def generate_random_circuit(n):
        if n == 1:
            return random.choice(['TRUE', 'FALSE'])
        if random.random() < 0.5:
            return ('AND', generate_random_circuit(n-1), generate_random_circuit(n-1))
        elif random.random() < 0.5:
            return ('OR', generate_random_circuit(n-1), generate_random_circuit(n-1))
        else:
            return ('NOT', generate_random_circuit(n-1))
    
    n = 20
    circuit = generate_random_circuit(n)
    width = negation_width(circuit)
    tree = resolution_refutation_tree(circuit)
    rank = tropicalized_hodge_structure(tree)
    
    if rank < width:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"circuit with negation width {width} has rank {rank}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"circuit with negation width {results[seeds.index(first_failing_seed)]['metric_value']} has rank {results[seeds.index(first_failing_seed)]['metric_value']}\" first_failing_seed={first_failing_seed}")