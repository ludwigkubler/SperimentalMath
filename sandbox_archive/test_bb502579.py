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

def generate_primes(n):
    primes = []
    sieve = [True] * (n + 1)
    for x in range(2, n + 1):
        if sieve[x]:
            primes.append(x)
            for i in range(x*x, n + 1, x):
                sieve[i] = False
    return primes

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def generate_gadget(k):
    gadget = {}
    for i in range(2**k):
        for j in range(2**k):
            if hamming_distance(bin(i)[2:].zfill(k), bin(j)[2:].zfill(k)) == 1:
                gadget[(i, j)] = (i ^ j, i & j)
    return gadget

def generate_random_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def generate_instances(gadget, n):
    instances = []
    for _ in range(n):
        x = generate_random_string(len(list(gadget.keys())[0][0]))
        y = generate_random_string(len(list(gadget.keys())[0][1]))
        instances.append((x, y))
    return instances

def protocol_pullback(gadget, instance, protocol):
    x, y = instance
    partition = []
    for i in range(2**len(x)):
        for j in range(2**len(y)):
            if (i, j) in gadget and gadget[(i, j)] == protocol(instance):
                partition.append((i, j))
    return partition

def compute_cover_multiplicity(partition):
    multiplicity = 0
    distances = {}
    for i in range(len(partition)):
        for j in range(i + 1, len(partition)):
            dist = hamming_distance(bin(partition[i])[2:].zfill(len(partition[0])), bin(partition[j])[2:].zfill(len(partition[0])))
            if dist not in distances:
                distances[dist] = 0
            distances[dist] += 1
    for dist, count in distances.items():
        multiplicity = max(multiplicity, count)
    return multiplicity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = 5
    n = 20
    gadget = generate_gadget(k)
    instances = generate_instances(gadget, n)
    
    results = []
    for c in range(1, 2 * k):
        protocol = lambda x: (int(x[0], 2) ^ int(x[1], 2), int(x[0], 2) & int(x[1], 2))
        partition = protocol_pullback(gadget, instances[0], protocol)
        multiplicity = compute_cover_multiplicity(partition)
        scale = max(hamming_distance(bin(i)[2:].zfill(k), bin(j)[2:].zfill(k)) for i in range(2**k) for j in range(2**k))
        
        alpha = math.log2(asdim_R(G) + 1)
        expected_multiplicity = 2**(c - alpha * Q(f))
        
        results.append({
            "metric_name": "Multiplicity",
            "metric_value": multiplicity,
            "instances_tested": 1,
            "conjecture_holds": multiplicity > expected_multiplicity,
            "counterexample": "" if multiplicity <= expected_multiplicity else f"Expected {expected_multiplicity}, got {multiplicity}"
        })
    
    return {
        "seed": seed,
        "metric_name": "Multiplicity",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": n * len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else min(result["counterexample"] for result in results)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")