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

def is_permutation(s1, s2):
    if len(s1) != len(s2):
        return False
    count = [0] * 26
    for c in s1:
        count[ord(c) - ord('a')] += 1
    for c in s2:
        if count[ord(c) - ord('a')] == 0:
            return False
        count[ord(c) - ord('a')] -= 1
    return True

def permute(s, perm):
    return ''.join(perm[ord(c) - ord('a')] for c in s)

def automorphism_group_rank(regex):
    alphabet = set(regex)
    if len(alphabet) > 26:
        return None
    perm = list(range(len(alphabet)))
    random.shuffle(perm)
    while True:
        if all(is_permutation(regex, permute(regex, perm)) for regex in [regex.replace(char, perm[i]) for i, char in enumerate(alphabet)]):
            return len(set(''.join(perm[ord(c) - ord('a')] for c in s) for s in [''.join(random.choice(list(alphabet)) for _ in range(len(regex))) for _ in range(10)]))
        random.shuffle(perm)

def frege_proof_depth(regex):
    # Placeholder function to simulate Frege proof depth calculation
    return len(regex) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    rank_sum = 0
    depth_sum = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        regex = ''.join(random.choice('ab') for _ in range(n))
        rank = automorphism_group_rank(regex)
        if rank is None:
            return {
                "metric_name": "rank(L_aut)",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        depth = frege_proof_depth(regex)
        rank_sum += rank
        depth_sum += depth
    
    mean_rank = rank_sum / instances_tested
    mean_depth = depth_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * depth for rank, depth in zip(range(instances_tested), range(instances_tested))) - rank_sum * depth_sum) / math.sqrt((instances_tested * sum(rank ** 2 for rank in range(instances_tested)) - rank_sum ** 2) * (instances_tested * sum(depth ** 2 for depth in range(instances_tested)) - depth_sum ** 2))
    
    return {
        "metric_name": "rank(L_aut)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")