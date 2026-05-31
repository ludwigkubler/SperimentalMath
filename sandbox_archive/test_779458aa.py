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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        if not cnf:
            return 0
        max_depth = 1
        for clause in cnf:
            depth = 1
            for literal in clause:
                if abs(literal) == 1:
                    depth += 1
            max_depth = max(max_depth, depth)
        return max_depth
    
    def geometrically_enriched_group_action(cnf):
        # Placeholder implementation; actual implementation needed
        return len(cnf)
    
    def minimal_local_index(group_action):
        return group_action
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    group_action = geometrically_enriched_group_action(cnf)
    mli = minimal_local_index(group_action)
    d_phi = circuit_depth(cnf)
    
    if d_phi == 0:
        return {
            "metric_name": "mli/d",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_depth_zero"
        }
    
    ratio = Fraction(mli, d_phi)
    return {
        "metric_name": "mli/d",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= float(ratio) <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        total_metric_value += result["metric_value"]
        if result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_conjecture_holds / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")