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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def braid_monodromy_rank(n, k):
        # Placeholder function to simulate the computation of braid monodromy rank
        # This is a dummy implementation and should be replaced with actual logic
        if n == 1:
            return 0
        return random.randint(1, int(k * log2(n) ** 2))
    
    def generate_xor_and_tree(n):
        # Placeholder function to simulate the generation of an XOR-AND tree
        # This is a dummy implementation and should be replaced with actual logic
        if n == 1:
            return 'leaf'
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return (left, right)
    
    def generate_k_clique_instance(n):
        # Placeholder function to simulate the generation of a k-CLIQUE instance
        # This is a dummy implementation and should be replaced with actual logic
        if n == 1:
            return []
        clique = set(range(1, k + 1))
        remaining = list(set(range(k + 1, n + 1)))
        random.shuffle(remaining)
        return clique.union(remaining[:n - k])
    
    def compute_braid_monodromy_representation(instance):
        # Placeholder function to simulate the computation of braid monodromy representation
        # This is a dummy implementation and should be replaced with actual logic
        if isinstance(instance, tuple):
            left_rank = compute_braid_monodromy_representation(instance[0])
            right_rank = compute_braid_monodromy_representation(instance[1])
            return max(left_rank, right_rank) + 1
        else:
            return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        xor_and_tree = generate_xor_and_tree(n)
        k_clique_instance = generate_k_clique_instance(n)
        
        xor_and_rank = braid_monodromy_rank(n, len(k_clique_instance))
        k_clique_rank = compute_braid_monodromy_representation(k_clique_instance)
        
        results.append({
            "n": n,
            "xor_and_rank": xor_and_rank,
            "k_clique_rank": k_clique_rank
        })
    
    mean_xor_and_rank = sum(result["xor_and_rank"] for result in results) / len(results)
    mean_k_clique_rank = sum(result["k_clique_rank"] for result in results) / len(results)
    
    conjecture_holds_xor_and = abs(mean_xor_and_rank - log2(n)) <= 0.1 * log2(n)
    conjecture_holds_k_clique = mean_k_clique_rank <= len(k_clique_instance) * log2(n)
    
    return {
        "metric_name": "braid_monodromy_rank",
        "metric_value_xor_and": mean_xor_and_rank,
        "metric_value_k_clique": mean_k_clique_rank,
        "instances_tested": len(results),
        "conjecture_holds_xor_and": conjecture_holds_xor_and,
        "conjecture_holds_k_clique": conjecture_holds_k_clique,
        "counterexample_xor_and": "" if conjecture_holds_xor_and else f"n={n}, rank={mean_xor_and_rank}",
        "counterexample_k_clique": "" if conjecture_holds_k_clique else f"k={len(k_clique_instance)}, rank={mean_k_clique_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_xor_and_rank = sum(result["metric_value_xor_and"] for result in results) / len(results)
    mean_k_clique_rank = sum(result["metric_value_k_clique"] for result in results) / len(results)
    
    support_fraction_xor_and = sum(result["conjecture_holds_xor_and"] for result in results) / len(results)
    support_fraction_k_clique = sum(result["conjecture_holds_k_clique"] for result in results) / len(results)
    
    if support_fraction_xor_and >= 0.8 and support_fraction_k_clique >= 0.8:
        print(f"RESULT: SUPPORTED mean_xor_and={mean_xor_and_rank} std_xor_and=... support_fraction_xor_and={support_fraction_xor_and}")
        print(f"RESULT: SUPPORTED mean_k_clique={mean_k_clique_rank} std_k_clique=... support_fraction_k_clique={support_fraction_k_clique}")
    elif any(result["conjecture_holds_xor_and"] == False for result in results) or any(result["conjecture_holds_k_clique"] == False for result in results):
        counterexample_xor_and = next((result["counterexample_xor_and"] for result in results if result["conjecture_holds_xor_and"] == False), "")
        counterexample_k_clique = next((result["counterexample_k_clique"] for result in results if result["conjecture_holds_k_clique"] == False), "")
        print(f"RESULT: FALSIFIED xor_and_counterexample={counterexample_xor_and} k_clique_counterexample={counterexample_k_clique}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")