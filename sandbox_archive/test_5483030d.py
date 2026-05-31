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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[i] and x in queue[j] for x in set(queue[i]) & set(queue[j])):
                        new_clause = [x for x in queue[i] if x not in queue[j]] + [y for y in queue[j] if -y not in queue[i]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(queue)
            queue.append(new_clause)
    
    def minimal_automorphic_rank(cnf):
        # Placeholder implementation; actual computation depends on the L-function mapping
        return random.random() * 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = minimal_automorphic_rank(cnf)
        width = resolution_width(cnf)
        ranks.append(rank)
        widths.append(width)
    
    if len(ranks) < 30:
        return {
            "metric_name": "minimal_automorphic_rank",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = 0
    for i in range(len(ranks)):
        correlation_coefficient += (ranks[i] - mean_rank) * (widths[i] - mean_width)
    correlation_coefficient /= math.sqrt(sum((x - mean_rank) ** 2 for x in ranks)) * math.sqrt(sum((y - mean_width) ** 2 for y in widths))
    
    if correlation_coefficient < 0.8:
        return {
            "metric_name": "minimal_automorphic_rank",
            "metric_value": correlation_coefficient,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "low_correlation"
        }
    
    return {
        "metric_name": "minimal_automorphic_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ranks = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(mean_ranks) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(mean_ranks)/len(mean_ranks):.2f} std={math.sqrt(sum((x - sum(mean_ranks)/len(mean_ranks))**2 for x in mean_ranks))/len(mean_ranks):.2f} support_fraction={support_fraction:.2f}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}"
    
    print(RESULT)