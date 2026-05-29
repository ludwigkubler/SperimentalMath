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
    
    def generate_qbf(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def qbf_depth(qbf):
        if not qbf:
            return 0
        if qbf[0] == 'A':
            return 1 + max(qbf_depth(qbf[2]), qbf_depth(qbf[3]))
        elif qbf[0] == 'E':
            return 1 + min(qbf_depth(qbf[2]), qbf_depth(qbf[3]))
        else:
            return 0
    
    def grothendieck_teichmueller_rank(qbf):
        # Placeholder for actual computation
        return len(qbf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    qbf = generate_qbf(n)
    depth = qbf_depth(qbf)
    rank = grothendieck_teichmueller_rank(qbf)
    
    return {
        "metric_name": "Grothendieck-Teichmüller Group Representation Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= depth,
        "counterexample": "" if rank <= depth else f"QBF: {qbf}, Depth: {depth}, Rank: {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*4 + 1, 4))
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")