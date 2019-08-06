# -*- coding: utf-8 -*-
# USER: Test
# Time: 2019/8/6 10:49


def reverse(l, i, j):
    while i < j:
        l[i], l[j] = l[j], l[i]
        i += 1
        j -= 1


def rotate(nums, k):
    """
    Do not return anything, modify nums in-place instead.
    """
    length = len(nums)
    k = k % length
    if k == length:
        return

    reverse(nums, 0, length - k - 1)
    print(nums)
    reverse(nums, length - k, length - 1)
    print(nums)
    reverse(nums, 0, length - 1)


def containsDuplicate(nums):
    length = len(nums)
    for i in range(length):
        for j in range(i + 1, length):
            print(i, j)
            if nums[i] == nums[j]:
                return True
    return False


def test_containsDuplicate():
    print(containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))
    print(containsDuplicate([1, 2, 3, 4]))
    print(containsDuplicate([1, 2, 3, 1]))


def singleNumber(nums) -> int:
    ret = 0
    for i in nums:
        ret ^= i
    return ret


def test_singleNumber():
    print(singleNumber([4, 1, 2, 1, 2]))
    print(singleNumber([2, 2, 1]))


if __name__ == '__main__':
    # a = [1, 2, 3, 4, 5, 6, 7]
    # rotate(a, 3)
    # print(a)
    # test_containsDuplicate()
    test_singleNumber()
