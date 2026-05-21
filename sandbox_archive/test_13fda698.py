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
    
    n = 30
    f = lambda x: sum(1 for i in range(n) if (x >> i) & 1 == 1) % 2
    
    def hypergeometric_moment(f, k):
        count = 0
        total = 0
        for _ in range(1000):  # Sample enough instances to get a good estimate
            x = random.randint(0, (1 << n) - 1)
            if f(x) == 1:
                count += 1
            total += 1
        return Fraction(count, total).limit_denominator()
    
    M_f = sum(hypergeometric_moment(f, k) for k in range(n))
    
    def communication_complexity(n):
        return n
    
    CC_XOR_n = communication_complexity(n)
    
    conjecture_holds = M_f == 0 or CC_XOR_n >= M_f * math.log2(n)
    counterexample = "M_f=0 or CC_XOR(n) < M_f log n" if not conjecture_holds else ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_XOR_n,
        "instances_tested": 1000,  # Number of samples for hypergeometric moment
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")