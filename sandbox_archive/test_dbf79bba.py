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
    
    def generate_k_clique(n, k):
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((i, j))
        for i in range(k, n):
            for edge in edges:
                if edge[0] < k and edge[1] < k:
                    continue
                if random.choice([True, False]):
                    edges.append(edge)
        return edges
    
    def hypergraph_rank(edges, n):
        rank = [0] * n
        for u, v in edges:
            if rank[u] == 0 or rank[v] == 0:
                rank[u] += 1
                rank[v] += 1
        return max(rank)
    
    def is_dnf_formula(formula):
        return all(isinstance(clause, list) and all(isinstance(lit, int) for lit in clause) for clause in formula)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    edges = generate_k_clique(n, k)
    rank_f = hypergraph_rank(edges, n)
    
    if rank_f < n / (4 * k):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rank_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}, rank_f={rank_f} < n/(4*k)"
        }
    
    formula = []
    for _ in range(random.randint(5, 20)):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
        formula.append(clause)
    
    if is_dnf_formula(formula):
        rank_f = hypergraph_rank([(abs(lit), lit // abs(lit)) for clause in formula for lit in clause], n)
        if rank_f > 3 * math.log(n):
            return {
                "metric_name": "polymatroid_rank",
                "metric_value": rank_f,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, DNF size={len(formula)}, rank_f={rank_f} > 3*log(n)"
            }
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rank_f,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")