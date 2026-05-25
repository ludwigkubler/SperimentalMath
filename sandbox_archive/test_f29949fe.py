# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(depth):
        if depth == 1:
            return ['A']
        else:
            p = 'P' + str(random.randint(1, 100))
            q = 'Q' + str(random.randint(1, 100))
            r = 'R' + str(random.randint(1, 100))
            return [f'{p} ∨ {q}', f'{r} → {p}', f'{r} → {q}', f'{r} ∧ ¬{p}', f'{r} ∧ ¬{q}']
    
    def resolution_tree(formula):
        clauses = formula[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause1 = clauses[i]
                    clause2 = clauses[j]
                    if any(not (c.startswith('¬') and c[1:] == literal) for literal in clause1.split()):
                        continue
                    new_clause = [literal for literal in clause1.split() if literal != '¬' + literal.split()[0]]
                    new_clause.extend([literal for literal in clause2.split() if literal not in new_clause])
                    if len(new_clause) > 0:
                        new_clauses.append(' ∨ '.join(new_clause))
            if set(new_clauses).issubset(set(clauses)):
                break
            clauses.extend(new_clauses)
        return clauses
    
    def minimal_rank(clauses):
        n = len(clauses)
        rank = [1] * n
        for i in range(n):
            for j in range(i + 1, n):
                if any(literal in clause2.split() for literal in clauses[i].split()):
                    rank[j] += 1
        return max(rank)
    
    def geometric_quantization_rank(depth):
        formula = tseitin_formula(depth)
        tree = resolution_tree(formula)
        return minimal_rank(tree)
    
    depth_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for depth in depth_values:
        rank = geometric_quantization_rank(depth)
        if rank < 2 ** (0.4 * depth):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": len(depth_values),
                "conjecture_holds": False,
                "counterexample": f"Depth {depth}, Rank {rank}"
            }
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = (sum((x - mean_rank) ** 2 for x in ranks) / len(ranks)) ** 0.5
    support_fraction = all(rank >= 2 ** (0.5 * depth) for rank, depth in zip(ranks, depth_values))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(depth_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")