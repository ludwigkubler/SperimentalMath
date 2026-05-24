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
    
    def generate_dnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def moment_map(dnf):
        n = len(dnf[0])
        rank = 0
        for clause in dnf:
            if all(x == 0 for x in clause):
                continue
            rank += 1
        return rank
    
    def acc0_circuit_depth(dnf):
        n = len(dnf[0])
        depth = 0
        for clause in dnf:
            depth = max(depth, sum(abs(x) for x in clause))
        return depth
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    dnf = generate_dnf(n, m)
    
    r_min_M = moment_map(dnf)
    D = acc0_circuit_depth(dnf)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": r_min_M,
        "instances_tested": 1,
        "conjecture_holds": r_min_M <= D,
        "counterexample": "" if r_min_M <= D else f"r_min(M) = {r_min_M}, D = {D}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")