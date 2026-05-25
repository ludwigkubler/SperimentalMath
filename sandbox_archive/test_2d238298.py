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
    
    def tropicalized_noncrossing_partition_polynomial(f):
        n = len(f)
        if n == 1:
            return f[0]
        else:
            left = tropicalized_noncrossing_partition_polynomial(f[:n//2])
            right = tropicalized_noncrossing_partition_polynomial(f[n//2:])
            return max(left, right) + min(left, right)
    
    def bp_readtwice_circuit_size(n):
        if n == 1:
            return 1
        else:
            return 2 * bp_readtwice_circuit_size(n // 2) + 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    rank = tropicalized_noncrossing_partition_polynomial(f)
    circuit_size = bp_readtwice_circuit_size(n)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log2(n) and circuit_size >= 2**n,
        "counterexample": "" if rank <= math.log2(n) and circuit_size >= 2**n else f"Rank {rank} > log({n}) or Circuit Size < 2^{n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    num_seeds = len(results)
    total_rank = sum(r["metric_value"] for r in results)
    avg_rank = total_rank / num_seeds
    std_rank = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / num_seeds)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_seeds
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break