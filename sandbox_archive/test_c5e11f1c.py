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
from itertools import permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(3, 10)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    T_M_size = sum(all(M[i][sigma[i]] == 1 for i in range(n)) for sigma in permutations(range(n)))
    if T_M_size < 2:
        return {
            "metric_name": "R_2",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "T_M_size < 2"
        }
    
    perm_q = sum(2 ** sum(i for i, x in enumerate(sigma) if sigma[i] > sigma[j]) for sigma in permutations(range(n)))
    det_q = sum((-1) ** sum(i for i, x in enumerate(sigma) if sigma[i] > sigma[j]) * 2 ** sum(i for i, x in enumerate(sigma) if sigma[i] > sigma[j]) for sigma in permutations(range(n)))
    
    R_2 = perm_q / max(1, abs(det_q))
    
    return {
        "metric_name": "R_2",
        "metric_value": R_2,
        "instances_tested": T_M_size,
        "conjecture_holds": R_2 >= math.sqrt(T_M_size) / (2 * n),
        "counterexample": "" if R_2 >= math.sqrt(T_M_size) / (2 * n) else f"R_2={R_2} < sqrt(|T_M|)/(2n)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    R_2_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(R_2_values)/len(R_2_values):.4f} std={math.sqrt(sum((x - sum(R_2_values)/len(R_2_values))**2 for x in R_2_values) / len(R_2_values)):.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unreachable")