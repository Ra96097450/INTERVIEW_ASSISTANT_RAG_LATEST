# Data Structures and Algorithms

## Hash Maps
A hash map stores key-value pairs and uses a hash function to determine where a key should be stored. Average-case lookup, insertion, and deletion are O(1).

Hash maps are useful for problems such as Two Sum, frequency counting, caching, and fast membership checks.

## Two Sum
The Two Sum problem asks for two numbers in an array whose sum equals a target.

An efficient approach uses a hash map. For each number x, calculate target - x and check whether that value has already been seen.

This reduces the typical brute-force O(n^2) approach to average O(n).

## Binary Search
Binary search works on sorted data. It repeatedly checks the middle element and eliminates half of the remaining search space.

Its time complexity is O(log n).

## Sliding Window
The sliding window technique maintains a range over an array or string and moves the boundaries efficiently. It is useful for problems involving contiguous subarrays or substrings.

Many sliding-window problems can be solved in O(n) instead of O(n^2).
