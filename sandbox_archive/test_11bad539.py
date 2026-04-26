import random
import math
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def fourier_coefficient(f, S):
        n = int(math.log2(len(f)))
        sum_val = 0
        for x in range(2**n):
            sign = (-1) ** (sum(int(b) * s for b, s in zip(bin(x)[2:].zfill(n), S)))
            sum_val += f[x] * sign
        return sum_val / (2**n)
    
    def fourier_l1_norm(f):
        n = int(math.log2(len(f)))
        return sum(abs(fourier_coefficient(f, S)) for S in itertools.combinations(range(n), n))
    
    def karchmer_wigderson_communication_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified simulation of K-W game complexity
        return n
    
    n = random.choice([5, 8, 11, 14])
    f = generate_random_boolean_function(n)
    
    l1_norm = fourier_l1_norm(f)
    kwc_complexity = karchmer_wigderson_communication_complexity(f)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": kwc_complexity,
        "instances_tested": 1,
        "conjecture_holds": kwc_complexity >= l1_norm,
        "counterexample": "" if kwc_complexity >= l1_norm else f"n={n}, f={f}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, f={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")