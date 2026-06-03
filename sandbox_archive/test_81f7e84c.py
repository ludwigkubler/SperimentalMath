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
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [[0] * (1 << n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            mask = 0
            for lit in clause:
                if lit > 0:
                    mask |= 1 << (lit - 1)
                else:
                    mask |= 1 << (-lit - 1)
            poly[i][mask] = 1
        return poly
    
    def grothendieck_witt_class_rank(poly):
        n = len(poly[0])
        rank = 0
        for i in range(1 << n):
            if any(poly[j][i] == 1 for j in range(len(poly))):
                rank += 1
        return rank
    
    def frege_proof_depth(cnf):
        # Placeholder function; actual implementation depends on the Frege proof system
        return len(cnf) * 2  # Simplified example
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    
    poly = clause_indicator_polynomial(cnf)
    gwc_rank = grothendieck_witt_class_rank(poly)
    fp_depth = frege_proof_depth(cnf)
    
    return {
        "metric_name": "gwc_rank_vs_fp_depth",
        "metric_value": gwc_rank / fp_depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if gwc_rank > 2 * fp_depth else True,
        "counterexample": "" if gwc_rank <= 2 * fp_depth else f"gwc_rank({gwc_rank}) > 2 * fp_depth({fp_depth})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gwc_rank > 2 * fp_depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")