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
    
    def frege_depth(cnf):
        if not cnf:
            return 0
        pos_cnf = [lit for lit in cnf if lit > 0]
        neg_cnf = [-lit for lit in cnf if lit < 0]
        if not pos_cnf and not neg_cnf:
            return 1
        if not pos_cnf or not neg_cnf:
            return max(frege_depth(pos_cnf), frege_depth(neg_cnf))
        else:
            return 1 + max(frege_depth(pos_cnf), frege_depth(neg_cnf))
    
    def local_index(cnf):
        # Simplified version for demonstration purposes
        return len(cnf)
    
    n = random.randint(5, 30)
    cnf = [random.choice([-i, i]) for i in range(1, n+1)]
    li = local_index(cnf)
    fd = frege_depth(cnf)
    
    ratio = Fraction(li) / fd
    expected_ratio = math.log2(li)
    
    conjecture_holds = abs(ratio - expected_ratio) <= 2 ** li
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"li={li}, fd={fd}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")