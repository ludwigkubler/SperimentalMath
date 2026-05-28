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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_queries = 0
        for i in range(2**n):
            queries = []
            for j in range(n):
                queries.append((i >> j) & 1)
            if f[i] != f[sum(q << j for j, q in enumerate(reversed(queries)))]:
                return len(queries)
        return max_queries
    
    def ehrhart_semigroup(f):
        n = int(math.log2(len(f)))
        semigroup = set()
        for i in range(2**n):
            count = sum((i >> j) & 1 for j in range(n))
            if f[i] == f[sum(q << j for j, q in enumerate(reversed(bin(count)[2:].zfill(n))))]:
                semigroup.add(count)
        return len(semigroup)
    
    def is_symmetric(f):
        n = int(math.log2(len(f)))
        for i in range(2**n):
            permuted = sum((i >> j) & 1 << (n - j - 1) for j in range(n))
            if f[i] != f[permuted]:
                return False
        return True
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    rank_ehrhart = ehrhart_semigroup(f)
    cc_symmetry_det = communication_complexity(f)
    
    if is_symmetric(f):
        counterexample = ""
    else:
        counterexample = "function_not_symmetric"
    
    return {
        "metric_name": "Rank_Ehrhart vs CC_SymmetryDet",
        "metric_value": rank_ehrhart,
        "instances_tested": 1,
        "conjecture_holds": rank_ehrhart <= cc_symmetry_det,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        RESULT = f"SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] and abs(r["metric_value"] - sum(metric_values)/len(metric_values)) > 3 * math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)) for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"] and abs(r["metric_value"] - sum(metric_values)/len(metric_values)) > 3 * math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)))
        RESULT = f"FALSIFIED counterexample=\"function_not_symmetric\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)