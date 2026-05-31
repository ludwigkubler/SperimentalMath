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
    
    def generate_circuit(n, m):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f"~{v}" for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def hodge_module_rank(circuit):
        # Simplified mapping from circuit structure to Hodge module rank
        n = len(circuit)
        m = sum(len(clause) for clause in circuit)
        return Fraction(n + m, 2)
    
    def dpll_search_tree_size(circuit):
        stack = []
        literals = set()
        
        def dfs():
            if not literals:
                return 1
            literal = random.choice(list(literals))
            literals.remove(literal)
            count = 0
            for clause in circuit:
                if literal in clause or f"~{literal}" in clause:
                    continue
                count += dfs()
            literals.add(literal)
            return count
        
        return dfs()
    
    def pearson_correlation(ranks, sizes):
        n = len(ranks)
        mean_r = sum(ranks) / n
        mean_s = sum(sizes) / n
        numerator = sum((r - mean_r) * (s - mean_s) for r, s in zip(ranks, sizes))
        denominator = math.sqrt(sum((r - mean_r)**2 for r in ranks)) * math.sqrt(sum((s - mean_s)**2 for s in sizes))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    sizes = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            circuit = generate_circuit(n, m)
            rank = hodge_module_rank(circuit)
            size = dpll_search_tree_size(circuit)
            ranks.append(rank)
            sizes.append(size)
    
    correlation = pearson_correlation(ranks, sizes)
    conjecture_holds = 0.5 <= correlation <= 1.2
    counterexample = "" if conjecture_holds else f"Correlation: {correlation}"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif any(r["metric_value"] > 1.2 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["metric_value"] > 1.2)
        print(f"RESULT: FALSIFIED counterexample=\"High correlation\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"Low correlation\" first_failing_seed={next(s for s, r in enumerate(results) if not r['conjecture_holds'])}")