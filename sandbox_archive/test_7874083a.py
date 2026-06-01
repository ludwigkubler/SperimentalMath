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

def is_planar(n, edges):
    if n <= 2:
        return True
    if len(edges) > 3 * (n - 2):
        return False
    for u in range(n):
        neighbors = [v for v, e in enumerate(edges) if u in e]
        if len(neighbors) >= 5:
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    for k in range(j + 1, len(neighbors)):
                        for l in range(k + 1, len(neighbors)):
                            if (neighbors[i], neighbors[j]) in edges and \
                               (neighbors[i], neighbors[k]) in edges and \
                               (neighbors[i], neighbors[l]) in edges and \
                               (neighbors[j], neighbors[k]) in edges and \
                               (neighbors[j], neighbors[l]) in edges and \
                               (neighbors[k], neighbors[l]) in edges:
                                return False
    return True

def generate_planar_graph(n):
    while True:
        edges = []
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.5 and is_planar(n, edges + [(u, v)]):
                    edges.append((u, v))
        if len(edges) == 3 * (n - 2):
            return edges

def quadratic_residues(p):
    residues = set()
    for i in range(1, p):
        residues.add(i * i % p)
    return residues

def communication_complexity(n, edges):
    # Simplified model: each edge requires one bit to communicate
    return n - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "communication_complexity"
    instances_tested = 0
    n_max = 0
    total_Q = 0
    total_g = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            p = random.randint(n + 1, 2 * n)
            residues = quadratic_residues(p)
            edges = generate_planar_graph(n)
            Q = len(residues & {e[0] * e[1] % p for e in edges})
            g = communication_complexity(n, edges)
            
            total_Q += Q
            total_g += g
            instances_tested += 1
    
    mean_Q = total_Q / instances_tested
    mean_g = total_g / instances_tested
    correlation_coefficient = (instances_tested * sum(Q * g for Q, g in zip([mean_Q] * instances_tested, [mean_g] * instances_tested)) - 
                               sum(Q) * sum(g)) / \
                              math.sqrt((instances_tested * sum(Q**2 for Q in [mean_Q] * instances_tested) - sum(Q)**2) *
                                        (instances_tested * sum(g**2 for g in [mean_g] * instances_tested) - sum(g)**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) >= 8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient=<{}>\" first_failing_seed={}".format(results[first_failing_seed]["metric_value"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")