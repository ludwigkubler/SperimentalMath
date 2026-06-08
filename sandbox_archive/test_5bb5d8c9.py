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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def poset_from_cnf(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        poset = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j and abs(i) < abs(j):
                        poset[abs(i)][abs(j)] = 1
        return poset
    
    def non_crossing_partition(poset, n):
        # Simplified version of the algorithm to find a non-crossing partition
        partition = [set() for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if poset[i][j] == 1:
                    partition[min(i, j)].add(max(i, j))
        return partition
    
    def frege_proof_depth(cnf):
        # Simplified version of the algorithm to estimate Frege proof depth
        depth = 0
        for clause in cnf:
            depth += len(clause)
        return depth
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        poset = poset_from_cnf(cnf)
        partition = non_crossing_partition(poset, n)
        f_phi = len(partition) - 1
        depth = frege_proof_depth(cnf)
        metric_values.append(f_phi)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    correlation_coefficient = sum((metric_values[i] - mean_value) * (depths[i] - mean_depth) for i in range(instances_tested)) / (instances_tested * std_value * std_depth)
    
    conjecture_holds = 0.8 <= correlation_coefficient <= 1 and O(n) <= mean_value <= Θ(n**2)
    counterexample = "" if conjecture_holds else "correlation_out_of_range"
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")

def O(n):
    return n

def Θ(n):
    return n**2