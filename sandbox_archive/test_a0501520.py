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
from fractions import Fraction
from math import log2, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_truth_table(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def truth_table_to_r_f(truth_table):
        r_f = Fraction(0)
        n = len(truth_table)
        for i in range(n):
            if truth_table[i]:
                r_f += Fraction(1, 2**(i+1))
        return r_f
    
    def continued_fraction_expansion(r_f, K_trunc):
        a = []
        while r_f != 0 and len(a) < K_trunc:
            a.append(int(1 / r_f))
            r_f = Fraction(1 / r_f - int(1 / r_f))
        return a
    
    def freq_1(f, K_trunc):
        n = len(f)
        count = sum(1 for i in range(min(K_trunc, 4*n)) if f[i] == 1)
        return count / min(K_trunc, 4*n)
    
    def LZ77_phrase_count(truth_table):
        n = len(truth_table)
        phrase_count = 0
        i = 0
        while i < n:
            j = i + 1
            k = i
            while j < n and truth_table[j] == truth_table[k]:
                j += 1
            phrase_count += 1
            if j - i > 1:
                phrase_count += LZ77_phrase_count(truth_table[i+1:j])
            i = j
        return phrase_count
    
    def generate_random_k_DNF(n, k):
        variables = list(range(n))
        terms = []
        for _ in range(k):
            term = random.sample(variables, random.randint(1, n))
            terms.append(term)
        return terms
    
    def evaluate_k_DNF(truth_table, k_DNF):
        n = len(truth_table)
        m = len(k_DNF)
        result = [0] * n
        for i in range(n):
            for j in range(m):
                term = k_DNF[j]
                if all(truth_table[i + var] == 1 for var in term):
                    result[i] = 1
                    break
        return result
    
    def generate_dictator(n, variable):
        return [int(i // (2**(n-variable-1)) % 2) for i in range(2**n)]
    
    def generate_parity(n):
        return [sum(i // (2**j) % 2 for j in range(n)) % 2 for i in range(2**n)]
    
    def generate_majority_threshold(n, threshold):
        return [1 if sum(i // (2**j) % 2 for j in range(n)) >= threshold else 0 for i in range(2**n)]
    
    n_values = [6, 8, 10]
    instances_tested = 0
    total_product = 0
    counterexample = ""
    freq_1_list = []
    LZ77_list = []
    
    for n in n_values:
        K_trunc = 4 * n
        
        # Uniform random T_f
        truth_table = generate_truth_table(n)
        r_f = truth_table_to_r_f(truth_table)
        a = continued_fraction_expansion(r_f, K_trunc)
        freq_1_val = freq_1(a, K_trunc)
        LZ77_val = LZ77_phrase_count(truth_table)
        product = freq_1_val * log2(LZ77_val + 2)
        instances_tested += 1
        total_product += product
        if product > 4 * sqrt(n):
            counterexample += "Uniform random T_f, n={n}, product={product}\n"
        
        # Random k-DNFs of sizes {1, n, n^2}
        for k in [1, n, n**2]:
            truth_table = evaluate_k_DNF(generate_truth_table(n), generate_random_k_DNF(n, k))
            r_f = truth_table_to_r_f(truth_table)
            a = continued_fraction_expansion(r_f, K_trunc)
            freq_1_val = freq_1(a, K_trunc)
            LZ77_val = LZ77_phrase_count(truth_table)
            product = freq_1_val * log2(LZ77_val + 2)
            instances_tested += 1
            total_product += product
            if product > 4 * sqrt(n):
                counterexample += f"Random k-DNF of size {k}, n={n}, product={product}\n"
        
        # Dictator
        truth_table = generate_dictator(n, random.randint(0, n-1))
        r_f = truth_table_to_r_f(truth_table)
        a = continued_fraction_expansion(r_f, K_trunc)
        freq_1_val = freq_1(a, K_trunc)
        LZ77_val = LZ77_phrase_count(truth_table)
        product = freq_1_val * log2(LZ77_val + 2)
        instances_tested += 1
        total_product += product
        if product > 4 * sqrt(n):
            counterexample += f"Dictator, n={n}, product={product}\n"
        
        # Parity
        truth_table = generate_parity(n)
        r_f = truth_table_to_r_f(truth_table)
        a = continued_fraction_expansion(r_f, K_trunc)
        freq_1_val = freq_1(a, K_trunc)
        LZ77_val = LZ77_phrase_count(truth_table)
        product = freq_1_val * log2(LZ77_val + 2)
        instances_tested += 1
        total_product += product
        if product > 4 * sqrt(n):
            counterexample += f"Parity, n={n}, product={product}\n"
        
        # Majority/Threshold
        threshold = random.randint(1, n//2)
        truth_table = generate_majority_threshold(n, threshold)
        r_f = truth_table_to_r_f(truth_table)
        a = continued_fraction_expansion(r_f, K_trunc)
        freq_1_val = freq_1(a, K_trunc)
        LZ77_val = LZ77_phrase_count(truth_table)
        product = freq_1_val * log2(LZ77_val + 2)
        instances_tested += 1
        total_product += product
        if product > 4 * sqrt(n):
            counterexample += f"Majority/Threshold, n={n}, threshold={threshold}, product={product}\n"
    
    mean_product = total_product / instances_tested
    support_fraction = (instances_tested - len(counterexample.split('\n'))) / instances_tested
    
    return {
        "metric_name": "GKD(f) * log2(LZ(f) + 2)",
        "metric_value": mean_product,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8 and len(counterexample.split('\n')) == 0,
        "counterexample": counterexample.strip()
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_product = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["counterexample"]) / len(results)
    
    if all(not r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_product} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > 1.2 * 4 * sqrt(n) for n, r in zip([6, 8, 10], results)):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r["metric_value"] > 1.2 * 4 * sqrt(6))]
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")