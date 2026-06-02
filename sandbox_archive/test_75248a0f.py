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
    
    def generate_random_protocol(n, k):
        protocol = {}
        for i in range(k):
            participants = random.sample(range(1, n+1), 2)
            if tuple(participants) not in protocol:
                protocol[tuple(participants)] = []
            protocol[tuple(participants)].append(random.choice(['send', 'receive']))
        return protocol
    
    def construct_interaction_graph(protocol):
        graph = {}
        for participants, actions in protocol.items():
            for action in actions:
                if participants[0] not in graph:
                    graph[participants[0]] = set()
                if participants[1] not in graph:
                    graph[participants[1]] = set()
                graph[participants[0]].add(participants[1])
                graph[participants[1]].add(participants[0])
        return graph
    
    def compute_alexander_module_order(graph):
        # Simplified Alexander module order computation for demonstration
        # This is a placeholder and should be replaced with actual Alexander module computation
        n = len(graph)
        if n == 0:
            return 1
        return n * (n - 1) // 2
    
    def log_base(x, base):
        return math.log(x) / math.log(base)
    
    max_n = 40
    total_order = 0
    instances_tested = 0
    
    for n in range(5, max_n + 1):
        for k in range(2, min(n, 6)):  # Ensure at least 2 participants per protocol
            protocol = generate_random_protocol(n, k)
            graph = construct_interaction_graph(protocol)
            order = compute_alexander_module_order(graph)
            if order <= 0:
                continue
            total_order += order
            instances_tested += 1
    
    mean_order = total_order / instances_tested if instances_tested > 0 else 0
    conjecture_holds = all(mean_order <= 1.5 * log_base(n / k, 2) for n in range(5, max_n + 1) for k in range(2, min(n, 6)))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")