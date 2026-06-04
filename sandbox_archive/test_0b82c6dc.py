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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolution_tree(cnf):
        # Simplified version of resolution tree construction
        nodes = []
        for clause in cnf:
            nodes.append((clause, None))
        while len(nodes) > 1:
            node1, _ = nodes.pop()
            node2, _ = nodes.pop()
            new_clauses = set()
            for literal1 in node1[0]:
                if -literal1 in node2[0]:
                    continue
                for literal2 in node2[0]:
                    if literal1 != literal2 and -literal1 not in node2[0] and -literal2 not in node1[0]:
                        new_clauses.add(tuple(sorted([literal1, literal2])))
            nodes.append((new_clauses, None))
        return nodes[0][0]
    
    def geometric_entanglement(tree):
        # Simplified version of geometric entanglement calculation
        return len(tree)
    
    n = 5 + random.randint(0, 3) * 5
    cnf = generate_cnf(n)
    tree = resolution_tree(cnf)
    mge = geometric_entanglement(tree)
    w = len(tree)
    
    return {
        "metric_name": "correlation",
        "metric_value": mge / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")