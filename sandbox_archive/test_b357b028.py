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
    
    def generate_regex(n):
        if n == 1:
            return random.choice("a|b")
        else:
            subregex = generate_regex(random.randint(1, n-1))
            return f"({subregex})*"
    
    def is_permutation(s1, s2):
        if len(s1) != len(s2):
            return False
        count = [0] * 26
        for char in s1:
            count[ord(char) - ord('a')] += 1
        for char in s2:
            if count[ord(char) - ord('a')] == 0:
                return False
            count[ord(char) - ord('a')] -= 1
        return True
    
    def automorphism_group_rank(regex):
        n = len(regex)
        alphabet = set()
        for char in regex:
            if char.isalpha():
                alphabet.add(char)
        k = len(alphabet)
        
        def permute(s, perm):
            return ''.join(perm[ord(c) - ord('a')] for c in s)
        
        perms = []
        for perm in itertools.permutations(alphabet):
            if all(is_permutation(regex, permute(regex, perm)) for regex in [regex.replace(char, perm[i]) for i, char in enumerate(alphabet)]):
                perms.append(perm)
        
        return len(perms)
    
    def frege_proof_depth(regex):
        # Placeholder function to simulate Frege proof depth
        # This is a dummy implementation and should be replaced with an actual calculation
        return len(regex) * 2
    
    n_max = 0
    instances_tested = 0
    rank_sum = 0.0
    depth_sum = 0.0
    
    for _ in range(30):
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        
        regex = generate_regex(n)
        rank = automorphism_group_rank(regex)
        depth = frege_proof_depth(regex)
        
        rank_sum += rank
        depth_sum += depth
        instances_tested += 1
    
    mean_rank = rank_sum / instances_tested
    mean_depth = depth_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * depth for rank, depth in zip(ranks, depths)) - rank_sum * depth_sum) / (math.sqrt(instances_tested * sum(rank**2 for rank in ranks) - rank_sum**2) * math.sqrt(instances_tested * sum(depth**2 for depth in depths) - depth_sum**2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")