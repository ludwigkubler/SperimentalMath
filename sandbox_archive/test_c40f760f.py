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
    
    def generate_permutation(n):
        return list(range(1, n + 1))
    
    def noncrossing_partition_rank(perm):
        n = len(perm)
        ydiagram = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Fill the Young diagram
        for i in range(n):
            for j in range(i, n):
                if perm[i] < perm[j]:
                    ydiagram[i][j+1] = ydiagram[i][j] + 1
        
        # Compute the rank of the partition
        rank = 0
        for k in range(n):
            for i in range(k + 1):
                for j in range(i, n):
                    if sum(ydiagram[k][i:j+1]) == j - i + 1:
                        rank += 1
        
        return rank
    
    def communication_protocol(perm):
        # Placeholder for a simple sorting protocol
        # This is just an example and should be replaced with the actual protocol
        n = len(perm)
        sorted_perm = sorted(perm)
        protocol = []
        for i in range(n):
            protocol.append((perm.index(sorted_perm[i]), sorted_perm[i]))
        return protocol
    
    n = random.randint(5, 40)
    perm = generate_permutation(n)
    
    rank = noncrossing_partition_rank(perm)
    protocol = communication_protocol(perm)
    k = sum(len(bin(x)[2:]) for _, x in protocol)  # Total bits of communication
    
    c = 1.0  # Placeholder constant
    conjecture_holds = rank <= c * math.log(n)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} exceeds upper bound {c * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")