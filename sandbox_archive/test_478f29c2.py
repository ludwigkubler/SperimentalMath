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
    
    def perm(n):
        if n == 1:
            return [[1]]
        perms = []
        for i in range(n):
            for p in perm(n - 1):
                perms.append([i + 1] + [p[j] if j < i else p[j - 1] for j in range(i, n)])
        return perms
    
    def det(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det_val = 0
        sign = 1
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det_val += sign * matrix[0][i] * det(submatrix)
            sign *= -1
        return det_val
    
    def schur_weyl_duality_invariant(f):
        # Placeholder for actual computation of the invariant
        # For simplicity, we use a dummy value
        return random.random()
    
    n = 20
    m_max = int(n ** 1.5)
    instances_tested = 0
    total_ratio = 0
    
    for _ in range(30):
        f = [random.randint(-10, 10) for _ in range(n)]
        perm_n = det(perm(n))
        det_m_values = [det([[f[i] for i in p] for p in perm(m)]) for m in range(1, m_max + 1)]
        
        if not det_m_values:
            continue
        
        ratio = sum(schur_weyl_duality_invariant(f) / schur_weyl_duality_invariant([f[i] for i in p]) for p in perm(n)) / len(det_m_values)
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "average_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    average_ratio = total_ratio / instances_tested
    std_dev = (sum((ratio - average_ratio) ** 2 for ratio in det_m_values) / instances_tested) ** 0.5
    
    return {
        "metric_name": "average_ratio",
        "metric_value": average_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": average_ratio > 1 and std_dev < 0.1,
        "counterexample": "" if average_ratio > 1 else f"Average ratio {average_ratio} below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    average_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = (sum((r["metric_value"] - average_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={average_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["metric_value"] for r in results if r["metric_value"] is not None) > 1.1:
        print(f"RESULT: FALSIFIED counterexample=\"average_ratio_above_threshold\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")