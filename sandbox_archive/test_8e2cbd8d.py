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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def poset_from_cnf(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        poset = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause[i+1:], start=i+1):
                    if lit1 > 0 and lit2 > 0:
                        poset[lit1][lit2] = 1
                        poset[lit2][lit1] = 1
        return poset
    
    def non_crossing_partition(poset, n):
        partition = []
        for i in range(1, n + 1):
            found = False
            for p in partition:
                if all(poset[i][j] == 0 for j in p):
                    p.append(i)
                    found = True
                    break
            if not found:
                partition.append([i])
        return partition
    
    def frege_proof_depth(cnf):
        # Placeholder function, actual implementation needed
        return random.randint(1, n * (n + 1) // 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poset = poset_from_cnf(cnf)
        partition = non_crossing_partition(poset, n)
        depth = frege_proof_depth(cnf)
        
        if not partition or not all(len(p) > 0 for p in partition):
            return {
                "metric_name": "non-crossing_partition_order",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        order = sum(len(p) for p in partition)
        results.append(order)
    
    mean_order = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_order) ** 2 for x in results) / len(results))
    correlation_coefficient = None
    
    return {
        "metric_name": "non-crossing_partition_order",
        "metric_value": mean_order,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1 and O(n) <= mean_order <= Θ(n**2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")

def O(n):
    return n

def Θ(n):
    return n**2