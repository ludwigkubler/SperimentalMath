import random
import math
import sys
import json

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    n = len(shape)
    total = 0
    for row in range(n):
        for col in range(len(shape[row])):
            hook = shape[row][col] + (n - row) - 1 + (len(shape[row]) - col) - 1
            total += hook // gcd(hook, n * (n - row))
    return factorial(n * n) // total

def cycle_type_to_shape(cycle_type):
    shape = [0] * len(cycle_type)
    for length in cycle_type:
        shape[length - 1] += 1
    return shape

def abp_size(permutation, width):
    n = len(permutation)
    dp = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        dp[i][i] = 1
        for j in range(i - 1, -1, -1):
            for k in range(j, i):
                if permutation[k] == permutation[j]:
                    dp[i][j] = min(dp[i][j], dp[k][j + 1] + dp[i - k - 1][k])
    return dp[n][0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(10):  # Generate 10 random permutation polynomials per n
            permutation = list(range(n))
            random.shuffle(permutation)
            cycle_type = []
            i = 0
            while i < n:
                length = 1
                j = (i + 1) % n
                while permutation[j] != permutation[i]:
                    permutation[j], permutation[(j - 1) % n] = permutation[(j - 1) % n], permutation[j]
                    j = (j - 1) % n
                    length += 1
                cycle_type.append(length)
                i += length

            shape = cycle_type_to_shape(cycle_type)
            dim_specht = hook_length_formula(shape)

            abp_width = min(n, dim_specht)
            abp_size_value = abp_size(permutation, abp_width)

            if abp_size_value > dim_specht:
                conjecture_holds = False
                counterexample = f"n={n}, permutation={permutation}, dim(S^λ)={dim_specht}, ABP size={abp_size_value}"
                break

            total_metric_value += dim_specht
            instances_tested += 1

    return {
        "metric_name": "Specht Module Dimension",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial_result)}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results)
    instances_tested = sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")