from collections import Counter

def solution(nums):
    answer = 100_000_000
    nH = Counter(nums)
    for n in nH:
        if nH[n] == n:
            answer = min(answer, n)

    if answer == 100_000_000:
        return -1

    return answer


print(solution([1, 2, 3, 1, 3, 3, 2, 4]))
print(solution([1, 2, 3, 3, 3, 2, 4, 5, 5, 5]))
print(solution([1, 1, 2, 5, 5, 5, 5, 5, 3, 3, 3, 3, 5]))
print(solution([7, 6, 7, 7, 8, 8, 8, 8, 7, 5, 7, 7, 7, 8, 8]))
print(solution(
    [11, 12, 5, 5, 3, 11, 7, 12, 15, 12, 12, 11, 12, 12, 7, 8, 12, 11, 12, 7, 12, 5, 15, 20, 15, 12, 15, 12, 15, 14,
     12]))
