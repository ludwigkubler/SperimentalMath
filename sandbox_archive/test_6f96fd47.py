# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_tree(cnf):
        # Simplified resolution tree construction
        leaves = set(range(1, n + 1))
        tree = {i: [] for i in range(1, n + 1)}
        for clause in cnf:
            if len(clause) == 2 and abs(clause[0]) != abs(clause[1]):
                leaves.remove(abs(clause[0]))
                leaves.remove(abs(clause[1]))
                tree[abs(clause[0])].append(abs(clause[1]))
                tree[abs(clause[1])].append(abs(clause[0]))
        return tree, len(leaves)
    
    def hodge_index(n):
        # Simplified Hodge index calculation
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    tree, l_F = resolution_tree(cnf)
    
    h_F = hodge_index(n)
    c = 1.0  # Placeholder constant
    log_l_F = math.log2(l_F) if l_F > 0 else float('inf')
    
    metric_value = h_F
    conjecture_holds = h_F <= c * log_l_F
    counterexample = "" if conjecture_holds else f"Counterexample: n={n}, m={m}, h(F)={h_F}, c*log2(l_F)={c*log_l_F}"
    
    return {
        "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 103, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")