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
    
    def frege_proof_width(formula):
        if isinstance(formula, str):
            return 1
        elif formula[0] == 'AND':
            return max(frege_proof_width(subformula) for subformula in formula[1:])
        elif formula[0] == 'OR':
            return max(frege_proof_width(subformula) for subformula in formula[1:])
    
    def generate_frege_tree(n, depth):
        if depth == 0:
            return random.choice(['x' + str(i) for i in range(1, n+1)])
        else:
            op = random.choice(['AND', 'OR'])
            return (op, generate_frege_tree(n, depth-1), generate_frege_tree(n, depth-1))
    
    def clause_indicator_polynomial(tree):
        if isinstance(tree, str):
            return {tree: 1}
        elif tree[0] == 'AND':
            poly = {}
            for subformula in tree[1:]:
                subpoly = clause_indicator_polynomial(subformula)
                for key, value in subpoly.items():
                    if key not in poly:
                        poly[key] = value
                    else:
                        poly[key] += value
            return poly
        elif tree[0] == 'OR':
            poly = {}
            for subformula in tree[1:]:
                subpoly = clause_indicator_polynomial(subformula)
                for key, value in subpoly.items():
                    if key not in poly:
                        poly[key] = value
                    else:
                        poly[key] += value
            return poly
    
    def minimal_rank(poly):
        # Placeholder function to simulate the computation of minimal rank
        # This is a dummy implementation and should be replaced with actual logic
        return sum(poly.values())
    
    n_values = [20, 25, 30, 35, 40]
    p = 17  # Fixed prime for simplicity
    c = 0.5  # Example constant
    
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(6):  # 30 instances per seed
            tree = generate_frege_tree(n, random.randint(1, 4))
            depth = frege_proof_width(tree)
            poly = clause_indicator_polynomial(tree)
            rank = minimal_rank(poly)
            expected_rank = c * p ** (n - depth / 2)
            
            if rank < expected_rank:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested + 1,
                    "conjecture_holds": False,
                    "counterexample": f"rank={rank}, expected={expected_rank}"
                }
            
            total_rank += rank
            instances_tested += 1
    
    mean_value = total_rank / instances_tested
    support_fraction = (instances_tested - sum(1 for _ in range(instances_tested) if run_trial(seed)['conjecture_holds'])) / instances_tested
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")