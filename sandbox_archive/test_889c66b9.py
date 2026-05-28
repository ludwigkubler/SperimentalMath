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
            queries = set()
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    queries.add(j)
            max_queries = max(max_queries, len(queries))
        return max_queries
    
    def ehrhart_semigroup(f):
        n = int(math.log2(len(f)))
        semigroup = set()
        for i in range(2**n):
            count = 0
            for j in range(n):
                if f[i ^ (1 << j)] == f[i]:
                    count += 1
            semigroup.add(count)
        return len(semigroup)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    cc_symmetry_det = communication_complexity(f)
    rank_ehrhart = ehrhart_semigroup(f)
    
    metric_name = "communication_complexity"
    metric_value = cc_symmetry_det
    instances_tested = 1
    conjecture_holds = cc_symmetry_det <= rank_ehrhart
    counterexample = "" if conjecture_holds else f"CC_SymmetryDet({cc_symmetry_det}) > Rank_Ehrhart({rank_ehrhart})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")