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
    
    n = random.randint(5, 30)
    instances_tested = 30
    
    def generate_disjointness_protocol(n):
        protocol = []
        for i in range(n):
            protocol.append(random.choice(['A', 'B']))
        return protocol
    
    def construct_twisted_group_representation(protocol):
        # Simplified mapping: each 'A' is mapped to (1, 0), each 'B' to (0, 1)
        representation = []
        for bit in protocol:
            if bit == 'A':
                representation.append([1, 0])
            else:
                representation.append([0, 1])
        return representation
    
    def calculate_minimal_rank(representation):
        # Calculate the rank of the matrix representation
        m = len(representation)
        n = len(representation[0])
        rank = 0
        
        for i in range(m):
            if all(representation[i][j] == 0 for j in range(n)):
                continue
            
            rank += 1
            for j in range(i + 1, m):
                if any(representation[j][k] != 0 for k in range(n)):
                    scale = representation[j][i] / representation[i][i]
                    for k in range(n):
                        representation[j][k] -= scale * representation[i][k]
        
        return rank
    
    total_rank = 0
    for _ in range(instances_tested):
        protocol = generate_disjointness_protocol(n)
        representation = construct_twisted_group_representation(protocol)
        rank = calculate_minimal_rank(representation)
        total_rank += rank
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= n**2 * math.log(n) * 0.95 and mean_rank <= n**2 * math.log(n) * 1.05
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected=n^2*log(n)"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")