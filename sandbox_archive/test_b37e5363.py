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
    
    def construct_symplectic_structure(f):
        n = len(f)
        leaves = []
        for i in range(2**n):
            leaf = []
            for j in range(n):
                if (i >> j) & 1:
                    leaf.append(j)
            leaves.append(leaf)
        return leaves
    
    def communication_complexity_rank(leaves):
        n = len(leaves[0])
        rank = 0
        for leaf in leaves:
            rank += len(leaf)
        return rank / n
    
    def minimal_geometric_entropy(n):
        # Simplified version of geometric entropy for demonstration purposes
        return -n * math.log2(1/n) if n > 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    communication_ranks = []
    entropies = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        leaves = construct_symplectic_structure(f)
        rank = communication_complexity_rank(leaves)
        entropy = minimal_geometric_entropy(n)
        communication_ranks.append(rank)
        entropies.append(entropy)
    
    correlation_coefficient = sum((r1 - mean_ranks[0]) * (e1 - mean_entropies[0])
                                  for r1, e1 in zip(communication_ranks, entropies)) / \
                              math.sqrt(sum((r1 - mean_ranks[0])**2
                                           for r1 in communication_ranks) *
                                        sum((e1 - mean_entropies[0])**2
                                            for e1 in entropies))
    
    mean_ranks = [sum(x)/len(x) for x in zip(*communication_ranks)]
    mean_entropies = [sum(x)/len(x) for x in zip(*entropies)]
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(x >= 0 for x in communication_ranks),
        "counterexample": "" if correlation_coefficient >= 0.7 and all(x >= 0 for x in communication_ranks) else "negative_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "negative_correlation" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"negative_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")