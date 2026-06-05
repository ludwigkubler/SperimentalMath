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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def binary_tree_from_function(f):
        n = int(math.log2(len(f)))
        tree = {}
        for i in range(n):
            tree[i] = []
            for j in range(2**(n-i-1)):
                if f[2*j] == 0:
                    tree[i].append((2*j, 2*j+1))
                else:
                    tree[i].append((2*j+1, 2*j))
        return tree
    
    def local_induction_dimension(tree):
        n = max(tree.keys())
        visited = [False] * (2**(n+1) - 1)
        stack = [(0, set())]
        
        while stack:
            node, covered = stack.pop()
            if not visited[node]:
                visited[node] = True
                for child in tree.get(node, []):
                    if child[0] not in covered and child[1] not in covered:
                        stack.append((child[0], covered.union({node})))
                        stack.append((child[1], covered.union({node})))
        
        return sum(1 for v in visited if v)
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        max_rank = 0
        for i in range(n):
            rank = 0
            for j in range(2**(n-i-1)):
                if f[2*j] != f[2*j+1]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_value = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        tree = binary_tree_from_function(f)
        mild = local_induction_dimension(tree)
        ccr = communication_complexity_rank(f)
        metric_value.append((mild, ccr))
    
    correlation_coefficient = 0
    mean_mild = sum(mild for mild, _ in metric_value) / len(metric_value)
    mean_ccr = sum(ccr for _, ccr in metric_value) / len(metric_value)
    
    for mild, ccr in metric_value:
        correlation_coefficient += (mild - mean_mild) * (ccr - mean_ccr)
    correlation_coefficient /= len(metric_value) * math.sqrt(sum((mild - mean_mild)**2 for mild, _ in metric_value)) * math.sqrt(sum((ccr - mean_ccr)**2 for _, ccr in metric_value))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metric_value),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_mild <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_mild <= 3 else "correlation_coefficient<0.8 or mean_mild>3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(r["counterexample"] == "correlation_coefficient<0.8 or mean_mild>3" for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["counterexample"] == "correlation_coefficient<0.8 or mean_mild>3")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8 or mean_mild>3\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")