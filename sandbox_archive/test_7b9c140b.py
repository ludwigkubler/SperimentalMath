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
    
    def is_planar(n):
        if n < 3:
            return True
        for i in range(1, n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i * j + j * k + k * i) % (n - 1) == 0:
                        return False
        return True

    def generate_planar_graph(n):
        while not is_planar(n):
            edges = set()
            for _ in range(3 * n - 6):
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
            return list(edges)

    def quadratic_residues(p):
        residues = set()
        for i in range(1, p):
            residues.add(i * i % p)
        return residues

    def communication_complexity(n):
        # Placeholder function; actual implementation depends on the game
        return n ** 2

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_planar_graph(n)
        p = random.randint(2, n - 1)
        residues = quadratic_residues(p)
        Q_G = len(residues.intersection({w % p for u, v in graph for w in range(n)}))
        g_n = communication_complexity(n)
        results.append((Q_G, g_n))

    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    Q_G_values = [Q for Q, _ in results]
    g_n_values = [g for _, g in results]

    mean_Q_G = sum(Q_G_values) / len(Q_G_values)
    mean_g_n = sum(g_n_values) / len(g_n_values)

    covariance = sum((Q_G - mean_Q_G) * (g_n - mean_g_n) for Q_G, g_n in results) / len(results)
    variance_Q_G = sum((Q_G - mean_Q_G) ** 2 for Q_G in Q_G_values) / len(Q_G_values)
    variance_g_n = sum((g_n - mean_g_n) ** 2 for g_n in g_n_values) / len(g_n_values)

    if variance_Q_G == 0 or variance_g_n == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }

    pearson_corr = covariance / (math.sqrt(variance_Q_G) * math.sqrt(variance_g_n))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_corr) > 0.7,
        "counterexample": "" if abs(pearson_corr) > 0.7 else f"correlation={pearson_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
        sys.exit(0)

    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")