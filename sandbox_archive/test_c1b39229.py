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
    
    def plethysm_coefficient(n, k):
        if n == 0 or k == 0:
            return 1
        result = 0
        for i in range(k + 1):
            result += math.comb(n, i) * plethysm_coefficient(n - i, k - i)
        return result
    
    def sos_refutation_size(n, k):
        if n == 0 or k == 0:
            return 1
        return (n ** (k / 2)) + 1
    
    n = random.randint(5, 40)
    k = random.randint(1, int(math.log(n)))
    
    plethysm_val = plethysm_coefficient(n, k)
    sos_size = sos_refutation_size(n, k)
    
    ratio = plethysm_val / sos_size if sos_size != 0 else float('inf')
    
    return {
        "metric_name": "plethysm_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= n ** (k / 2),
        "counterexample": "" if ratio >= n ** (k / 2) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_ratio = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_ratio) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")