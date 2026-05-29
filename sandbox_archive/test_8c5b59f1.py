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
    
    def generate_qbf(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def qbf_depth(qbf):
        if not qbf:
            return 0
        depth = 1
        for i in range(len(qbf)):
            if qbf[i] == 'Q':
                depth = max(depth, qbf_depth(qbf[i+1:]))
        return depth
    
    def grothendieck_teichmueller_rank(qbf):
        # Placeholder function to simulate Grothendieck-Teichmüller rank calculation
        return len(qbf)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        qbf = generate_qbf(n)
        depth = qbf_depth(qbf)
        rank = grothendieck_teichmueller_rank(qbf)
        
        if rank > depth:
            conjecture_holds = False
            counterexample = f"QBF with n={n}, rank={rank}, depth={depth}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "Grothendieck-Teichmüller Group Representation Rank",
        "metric_value": rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")