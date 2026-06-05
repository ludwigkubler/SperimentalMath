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
    
    def shannon_entropy(p):
        return -sum(x * math.log2(x) for x in p if x > 0)

    n = 10  # Start with a small instance size and increase as needed
    instances_tested = 0
    total_entropy = 0.0
    n_max = n
    
    while True:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        protocol = {}
        
        # Simulate a simple communication protocol (e.g., random assignment)
        for x in range(2**n):
            y = random.choice(f)
            if y not in protocol:
                protocol[y] = []
            protocol[y].append(x)
        
        # Compute the geometric entropy
        p = [len(v) / 2**n for v in protocol.values()]
        entropy = shannon_entropy(p)
        total_entropy += entropy
        instances_tested += 1
        
        if n_max < n:
            n_max = n
        
        if instances_tested >= 30:
            break
        
        n += 5  # Increase instance size to test for asymptotic behavior
    
    metric_value = total_entropy / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "geometric entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.3:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")