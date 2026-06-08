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
from math import factorial, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if len(set(clause)) > 1:
                clauses.append(clause)
        return clauses
    
    def poset_from_cnf(cnf):
        n = max(abs(lit) for lit in cnf[0])
        poset = [[False] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, lit_i in enumerate(clause):
                for j, lit_j in enumerate(clause):
                    if i < j and (lit_i > 0 and lit_j < 0 or lit_i < 0 and lit_j > 0):
                        poset[abs(lit_i)][abs(lit_j)] = True
        return poset
    
    def non_crossing_partition_size(poset, n):
        if n == 1:
            return 1
        partition = [set([i]) for i in range(1, n + 1)]
        while len(partition) > 1:
            merged = False
            for i in range(len(partition)):
                for j in range(i + 1, len(partition)):
                    if all(poset[x][y] == poset[y][x] for x in partition[i] for y in partition[j]):
                        partition[i].update(partition[j])
                        del partition[j]
                        merged = True
                        break
                if merged:
                    break
            if not merged:
                return len(partition)
        return 1
    
    def frege_proof_depth(cnf):
        n = max(abs(lit) for lit in cnf[0])
        depth = [0] * (n + 1)
        stack = []
        for clause in cnf:
            for lit in clause:
                if lit > 0 and depth[lit] == 0:
                    stack.append(lit)
                    depth[lit] = 1
        while stack:
            lit = stack.pop()
            for i in range(1, n + 1):
                if poset[lit][i]:
                    depth[i] = max(depth[i], depth[lit] + 1)
                    if depth[i] > len(stack):
                        stack.append(i)
        return max(depth)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        poset = poset_from_cnf(cnf)
        f_phi = non_crossing_partition_size(poset, n)
        depth = frege_proof_depth(cnf)
        results.append((n, f_phi, depth))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, f_phi_values, depth_values = zip(*results)
    mean_f_phi = sum(f_phi_values) / len(f_phi_values)
    mean_depth = sum(depth_values) / len(depth_values)
    correlation_coefficient = (sum((f_phi - mean_f_phi) * (depth - mean_depth) for f_phi, depth in zip(f_phi_values, depth_values)) /
                               sqrt(sum((f_phi - mean_f_phi) ** 2 for f_phi in f_phi_values) *
                                    sum((depth - mean_depth) ** 2 for depth in depth_values)))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(f_phi_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1 and O(n) <= mean_f_phi <= Θ(n**2),
        "counterexample": "" if 0.8 <= correlation_coefficient <= 1 else f"mean_f_phi={mean_f_phi}, mean_depth={mean_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")