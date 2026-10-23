"""More problems for data/problems.json (warm-ups through binary search). See problems_src.py for the format."""
from problems_src import add, rints, R
import problems_more2  # noqa: F401 (linked lists onward)

# ------------------------------------------------------------------ WARM-UPS
add(id="celsius-to-fahrenheit", title="Celsius to Fahrenheit", difficulty="Easy", cat="basics", tags=["Math"],
 desc=["Convert a temperature from degrees Celsius to degrees Fahrenheit using `F = C × 9 / 5 + 32`."],
 constraints=["-273.15 <= celsius <= 10^4"], params=["celsius"], fn={"py":"to_fahrenheit","js":"toFahrenheit"}, cmp="float",
 examples=[[100],[0],[-40]], tests=[[100],[0],[-40],[37],[-273.15],[21.5]],
 hints=["Translate the formula directly.","Multiply before dividing, or use 1.8."],
 editorial=["A direct translation of the formula. -40 is the one temperature where both scales agree, which makes a nice sanity check."],
 complexity="O(1).",
 py='''def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32''',
 js='''function toFahrenheit(celsius) {
  return celsius * 9 / 5 + 32;
}''')

add(id="count-words", title="Count the Words", difficulty="Easy", cat="basics", tags=["Strings"],
 desc=["Return how many words are in `sentence`. Words are separated by one or more spaces, and the sentence may start or end with spaces."],
 constraints=["0 <= sentence.length <= 10^4"], params=["sentence"], fn={"py":"count_words","js":"countWords"},
 examples=[["Hello world"],["  many   spaces here  "]], tests=[["Hello world"],["  many   spaces here  "],[""],["   "],["one"],["a b c d e f"]],
 hints=["Splitting on whitespace gives you the words.","In Python, `split()` with no argument ignores repeated spaces. In JavaScript, trim first and split on `/\\s+/`."],
 editorial=["Split on runs of whitespace and count the pieces. The edge case is an empty or all-space string, which has zero words (in JavaScript, `\"\".split(/\\s+/)` gives `[\"\"]`, so trim and check for empty first)."],
 complexity="O(n) time and space.",
 py='''def count_words(sentence):
    return len(sentence.split())''',
 js='''function countWords(sentence) {
  const t = sentence.trim();
  return t === "" ? 0 : t.split(/\\s+/).length;
}''')

add(id="palindrome-number", title="Palindrome Number", difficulty="Easy", cat="basics", tags=["Math"],
 desc=["Return `true` if the integer `x` reads the same backwards as forwards. Negative numbers are never palindromes (the `-` is only at the front)."],
 constraints=["-2^31 <= x <= 2^31 - 1"], params=["x"], fn={"py":"is_palindrome_number","js":"isPalindromeNumber"},
 examples=[[121],[-121],[10]], tests=[[121],[-121],[10],[0],[7],[1221],[12321],[123]],
 hints=["Converting to a string is the quick way.","Without strings: build the reversed number with `% 10` and `// 10`."],
 editorial=["Reverse the digits arithmetically (or compare the string with its reverse). Negative numbers fail immediately, and numbers ending in 0 can only be palindromes if they are 0."],
 complexity="O(d) for d digits.",
 py='''def is_palindrome_number(x):
    if x < 0:
        return False
    original, rev = x, 0
    while x > 0:
        rev = rev * 10 + x % 10
        x //= 10
    return rev == original''',
 js='''function isPalindromeNumber(x) {
  const s = String(x);
  return s === [...s].reverse().join("");
}''')

add(id="first-unique-char", title="First Unique Character", difficulty="Easy", cat="basics", tags=["Strings","Hash Table"],
 desc=["Return the index of the first character in `s` that appears exactly once, or `-1` if there is none."],
 constraints=["1 <= s.length <= 10^5","lowercase English letters"], params=["s"], fn={"py":"first_uniq_char","js":"firstUniqChar"},
 examples=[["leetcode"],["loveleetcode"],["aabb"]], tests=[["leetcode"],["loveleetcode"],["aabb"],["z"],["abcabd"],["xxyz"]],
 hints=["Count every character first.","Then scan again and return the first index whose count is 1."],
 editorial=["Two passes: count characters with a dictionary, then find the first position whose character has count 1."],
 complexity="O(n) time, O(1) space (26 letters).",
 py='''def first_uniq_char(s):
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i
    return -1''',
 js='''function firstUniqChar(s) {
  const count = {};
  for (const ch of s) count[ch] = (count[ch] || 0) + 1;
  for (let i = 0; i < s.length; i++) if (count[s[i]] === 1) return i;
  return -1;
}''')

add(id="running-sum", title="Running Sum of an Array", difficulty="Easy", cat="basics", tags=["Arrays","Prefix Sum"],
 desc=["Return a list where element `i` is the sum of `nums[0]` through `nums[i]`."],
 constraints=["1 <= nums.length <= 1000"], params=["nums"], fn={"py":"running_sum","js":"runningSum"},
 examples=[[[1,2,3,4]],[[3,1,2,10,1]]], tests=[[[1,2,3,4]],[[3,1,2,10,1]],[[5]],[[-1,1,-1,1]],[[0,0,0]]],
 hints=["Keep a running total as you walk the list.","Append the total after adding each number."],
 editorial=["Accumulate as you go. This **prefix sum** is a building block: with it, the sum of any range `i..j` is `prefix[j] - prefix[i-1]` in O(1)."],
 complexity="O(n) time.",
 py='''def running_sum(nums):
    out, total = [], 0
    for x in nums:
        total += x
        out.append(total)
    return out''',
 js='''function runningSum(nums) {
  let total = 0;
  return nums.map(x => (total += x));
}''')

add(id="max-consecutive-ones", title="Max Consecutive Ones", difficulty="Easy", cat="basics", tags=["Arrays"],
 desc=["`nums` contains only 0s and 1s. Return the length of the longest run of consecutive 1s."],
 constraints=["1 <= nums.length <= 10^5"], params=["nums"], fn={"py":"find_max_consecutive_ones","js":"findMaxConsecutiveOnes"},
 examples=[[[1,1,0,1,1,1]],[[1,0,1,1,0,1]]], tests=[[[1,1,0,1,1,1]],[[1,0,1,1,0,1]],[[0]],[[1]],[[0,0,1,1,1,1,0]]],
 hints=["Track the current run and the best run.","Reset the current run to 0 on a 0."],
 editorial=["One pass with two counters: the current streak and the best streak seen."],
 complexity="O(n) time, O(1) space.",
 py='''def find_max_consecutive_ones(nums):
    best = run = 0
    for x in nums:
        run = run + 1 if x == 1 else 0
        best = max(best, run)
    return best''',
 js='''function findMaxConsecutiveOnes(nums) {
  let best = 0, run = 0;
  for (const x of nums) { run = x === 1 ? run + 1 : 0; best = Math.max(best, run); }
  return best;
}''')

add(id="plus-one", title="Plus One", difficulty="Easy", cat="basics", tags=["Arrays","Math"],
 desc=["A non-negative integer is given as a list of its digits, most significant first. Add one and return the new list of digits."],
 constraints=["1 <= digits.length <= 100","No leading zeros except the number 0"], params=["digits"], fn={"py":"plus_one","js":"plusOne"},
 examples=[[[1,2,3]],[[9,9]]], tests=[[[1,2,3]],[[9,9]],[[0]],[[9]],[[1,9,9]],[[9,8,9]]],
 hints=["Work from the last digit backwards, like adding by hand.","A 9 becomes 0 and carries; if every digit carries, add a 1 in front."],
 editorial=["Walk from the end: if the digit is less than 9, increment it and return. Otherwise set it to 0 and continue. If the loop finishes, the number was all 9s, so prepend 1."],
 complexity="O(n) time.",
 py='''def plus_one(digits):
    digits = digits[:]
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits''',
 js='''function plusOne(digits) {
  const d = [...digits];
  for (let i = d.length - 1; i >= 0; i--) {
    if (d[i] < 9) { d[i]++; return d; }
    d[i] = 0;
  }
  return [1, ...d];
}''')

# ------------------------------------------------------------------ ARRAYS & HASHING
add(id="isomorphic-strings", title="Isomorphic Strings", difficulty="Easy", cat="arrays", tags=["String","Hash Table"],
 desc=["Two strings are isomorphic if the characters of `s` can be replaced to get `t`, where every occurrence of a character maps to the same character and no two characters map to the same one. Return whether `s` and `t` are isomorphic."],
 constraints=["1 <= s.length == t.length <= 5 × 10^4"], params=["s","t"], fn={"py":"is_isomorphic","js":"isIsomorphic"},
 examples=[["egg","add"],["foo","bar"],["paper","title"]], tests=[["egg","add"],["foo","bar"],["paper","title"],["badc","baba"],["a","b"],["ab","aa"]],
 hints=["One map is not enough: `ab` → `aa` must fail.","Keep a map in each direction, or compare the index of each character's first appearance."],
 editorial=["Maintain `s→t` and `t→s` maps. For each pair, if either side already maps somewhere different, fail. Two maps enforce a one-to-one mapping."],
 complexity="O(n) time, O(1) space for a fixed alphabet.",
 py='''def is_isomorphic(s, t):
    a, b = {}, {}
    for x, y in zip(s, t):
        if a.setdefault(x, y) != y or b.setdefault(y, x) != x:
            return False
    return True''',
 js='''function isIsomorphic(s, t) {
  const pattern = str => [...str].map(c => str.indexOf(c)).join(",");
  return pattern(s) === pattern(t);
}''')

add(id="intersection-of-arrays", title="Intersection of Two Arrays", difficulty="Easy", cat="arrays", tags=["Array","Hash Set"],
 desc=["Return the distinct values that appear in both `nums1` and `nums2`, in any order."],
 constraints=["1 <= nums1.length, nums2.length <= 1000"], params=["nums1","nums2"], fn={"py":"intersection","js":"intersection"}, cmp="unordered",
 examples=[[[1,2,2,1],[2,2]],[[4,9,5],[9,4,9,8,4]]], tests=[[[1,2,2,1],[2,2]],[[4,9,5],[9,4,9,8,4]],[[1],[2]],[[3,3,3],[3]],[[1,2,3],[3,2,1]]],
 hints=["Sets remove duplicates and test membership in O(1).","Set intersection: `&` in Python, a filter with `has` in JavaScript."],
 editorial=["Turn one array into a set and keep the distinct values of the other that are in it."],
 complexity="O(n + m) time.",
 py='''def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))''',
 js='''function intersection(a, b) {
  const s = new Set(a);
  return [...new Set(b)].filter(x => s.has(x));
}''')

add(id="subarray-sum-k", title="Subarray Sum Equals K", difficulty="Medium", cat="arrays", tags=["Array","Hash Table","Prefix Sum"],
 desc=["Return the number of contiguous, non-empty subarrays of `nums` whose sum is exactly `k`. Numbers may be negative."],
 constraints=["1 <= nums.length <= 2 × 10^4","-1000 <= nums[i] <= 1000"], params=["nums","k"], fn={"py":"subarray_sum","js":"subarraySum"},
 examples=[[[1,1,1],2],[[1,2,3],3]], tests=[[[1,1,1],2],[[1,2,3],3],[[1],0],[[0,0,0],0],[[1,-1,1,-1],0],[[3,4,7,2,-3,1,4,2],7],[rints(3000,-10,10),5]],
 hints=["A sliding window fails with negative numbers.","With prefix sums, sum(i..j) = prefix[j] − prefix[i−1]. Count how many earlier prefixes equal `prefix − k`."],
 editorial=["Walk the array keeping a running prefix sum and a dictionary counting how often each prefix has occurred (starting with `{0: 1}`). At each step, every earlier prefix equal to `prefix - k` ends a subarray summing to `k` here."],
 complexity="O(n) time, O(n) space.",
 py='''def subarray_sum(nums, k):
    seen = {0: 1}
    total = count = 0
    for x in nums:
        total += x
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count''',
 js='''function subarraySum(nums, k) {
  const seen = new Map([[0, 1]]);
  let total = 0, count = 0;
  for (const x of nums) {
    total += x;
    count += seen.get(total - k) || 0;
    seen.set(total, (seen.get(total) || 0) + 1);
  }
  return count;
}''')

add(id="rotate-image", title="Rotate Image", difficulty="Medium", cat="arrays", tags=["Matrix","In-place"],
 desc=["Rotate the `n × n` matrix 90 degrees clockwise **in place**. The judge inspects `matrix` after your function returns."],
 constraints=["1 <= n <= 20"], params=["matrix"], fn={"py":"rotate","js":"rotate"}, inplace=0,
 examples=[[[[1,2,3],[4,5,6],[7,8,9]]]], tests=[[[[1,2,3],[4,5,6],[7,8,9]]],[[[1]]],[[[1,2],[3,4]]],[[[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]]],
 hints=["Rotation = transpose (swap across the diagonal) then reverse each row.","Swap `m[i][j]` with `m[j][i]` only for `j > i`."],
 editorial=["Transpose the matrix in place, then reverse every row. Both steps are in place, so no extra matrix is needed."],
 complexity="O(n²) time, O(1) space.",
 py='''def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()''',
 js='''function rotate(m) {
  const n = m.length;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) [m[i][j], m[j][i]] = [m[j][i], m[i][j]];
  for (const row of m) row.reverse();
}''')

add(id="spiral-matrix", title="Spiral Matrix", difficulty="Medium", cat="arrays", tags=["Matrix","Simulation"],
 desc=["Return all elements of the `m × n` matrix in spiral order: right along the top, down the right side, left along the bottom, up the left side, then inwards."],
 constraints=["1 <= m, n <= 10"], params=["matrix"], fn={"py":"spiral_order","js":"spiralOrder"},
 examples=[[[[1,2,3],[4,5,6],[7,8,9]]],[[[1,2,3,4],[5,6,7,8],[9,10,11,12]]]], tests=[[[[1,2,3],[4,5,6],[7,8,9]]],[[[1,2,3,4],[5,6,7,8],[9,10,11,12]]],[[[7]]],[[[1],[2],[3]]],[[[1,2,3]]],[[[1,2],[3,4],[5,6]]]],
 hints=["Keep four boundaries: top, bottom, left, right.","After each side, move that boundary inwards; stop when they cross."],
 editorial=["Shrink four boundaries as you peel off the outer ring. Guard the bottom row and left column with `top <= bottom` and `left <= right` checks so single rows or columns aren't visited twice."],
 complexity="O(m × n) time.",
 py='''def spiral_order(matrix):
    out = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            out.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):
            out.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                out.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                out.append(matrix[i][left])
            left += 1
    return out''',
 js='''function spiralOrder(m) {
  const out = [];
  let top = 0, bottom = m.length - 1, left = 0, right = m[0].length - 1;
  while (top <= bottom && left <= right) {
    for (let j = left; j <= right; j++) out.push(m[top][j]);
    top++;
    for (let i = top; i <= bottom; i++) out.push(m[i][right]);
    right--;
    if (top <= bottom) { for (let j = right; j >= left; j--) out.push(m[bottom][j]); bottom--; }
    if (left <= right) { for (let i = bottom; i >= top; i--) out.push(m[i][left]); left++; }
  }
  return out;
}''')

add(id="set-matrix-zeroes", title="Set Matrix Zeroes", difficulty="Medium", cat="arrays", tags=["Matrix","In-place"],
 desc=["If an element of `matrix` is 0, set its entire row and column to 0. Do it **in place**; the judge inspects `matrix` afterwards."],
 constraints=["1 <= m, n <= 200"], params=["matrix"], fn={"py":"set_zeroes","js":"setZeroes"}, inplace=0,
 examples=[[[[1,1,1],[1,0,1],[1,1,1]]],[[[0,1,2,0],[3,4,5,2],[1,3,1,5]]]], tests=[[[[1,1,1],[1,0,1],[1,1,1]]],[[[0,1,2,0],[3,4,5,2],[1,3,1,5]]],[[[1]]],[[[0]]],[[[1,2],[3,0]]]],
 hints=["Don't zero things while scanning, or new zeros spread further.","Record which rows and columns contain a zero first, then apply."],
 editorial=["First pass: collect the rows and columns that contain a zero. Second pass: zero every cell in those rows or columns. (The O(1)-space trick stores these markers in the first row and column.)"],
 complexity="O(m × n) time, O(m + n) space.",
 py='''def set_zeroes(matrix):
    rows = {i for i, row in enumerate(matrix) for x in row if x == 0}
    cols = {j for row in matrix for j, x in enumerate(row) if x == 0}
    for i, row in enumerate(matrix):
        for j in range(len(row)):
            if i in rows or j in cols:
                row[j] = 0''',
 js='''function setZeroes(m) {
  const rows = new Set(), cols = new Set();
  m.forEach((row, i) => row.forEach((x, j) => { if (x === 0) { rows.add(i); cols.add(j); } }));
  m.forEach((row, i) => row.forEach((_, j) => { if (rows.has(i) || cols.has(j)) row[j] = 0; }));
}''')

# ------------------------------------------------------------------ TWO POINTERS
add(id="squares-sorted-array", title="Squares of a Sorted Array", difficulty="Easy", cat="two-pointers", tags=["Array","Two Pointers"],
 desc=["`nums` is sorted in non-decreasing order and may contain negatives. Return the squares of each number, also sorted, in O(n)."],
 constraints=["1 <= nums.length <= 10^4"], params=["nums"], fn={"py":"sorted_squares","js":"sortedSquares"},
 examples=[[[-4,-1,0,3,10]],[[-7,-3,2,3,11]]], tests=[[[-4,-1,0,3,10]],[[-7,-3,2,3,11]],[[1]],[[-5,-3,-1]],[[0,0,1]],[sorted(rints(2000,-10000,10000))]],
 hints=["The largest square is at one of the two ends.","Fill the output from the back with two pointers."],
 editorial=["The biggest absolute value is always at an end of the sorted array. Compare the two ends, write the larger square at the back of the output, move that pointer inwards, repeat."],
 complexity="O(n) time.",
 py='''def sorted_squares(nums):
    out = [0] * len(nums)
    lo, hi = 0, len(nums) - 1
    for k in range(len(nums) - 1, -1, -1):
        if abs(nums[lo]) > abs(nums[hi]):
            out[k] = nums[lo] ** 2
            lo += 1
        else:
            out[k] = nums[hi] ** 2
            hi -= 1
    return out''',
 js='''function sortedSquares(nums) {
  const out = new Array(nums.length);
  let lo = 0, hi = nums.length - 1;
  for (let k = nums.length - 1; k >= 0; k--) {
    if (Math.abs(nums[lo]) > Math.abs(nums[hi])) out[k] = nums[lo] ** 2, lo++;
    else out[k] = nums[hi] ** 2, hi--;
  }
  return out;
}''')

add(id="is-subsequence", title="Is Subsequence", difficulty="Easy", cat="two-pointers", tags=["String","Two Pointers"],
 desc=["Return `true` if `s` is a subsequence of `t`: you can delete some (or no) characters of `t`, without reordering the rest, to get `s`."],
 constraints=["0 <= s.length <= 100","0 <= t.length <= 10^4"], params=["s","t"], fn={"py":"is_subsequence","js":"isSubsequence"},
 examples=[["abc","ahbgdc"],["axc","ahbgdc"]], tests=[["abc","ahbgdc"],["axc","ahbgdc"],["","abc"],["abc",""],["aaa","aa"],["ace","abcde"]],
 hints=["Walk through `t` once.","Advance a pointer in `s` each time its current character matches."],
 editorial=["Greedy matching: scan `t`, and whenever the current character equals the next unmatched character of `s`, advance in `s`. If you match all of `s`, it's a subsequence."],
 complexity="O(|t|) time, O(1) space.",
 py='''def is_subsequence(s, t):
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)''',
 js='''function isSubsequence(s, t) {
  let i = 0;
  for (const ch of t) if (i < s.length && s[i] === ch) i++;
  return i === s.length;
}''')

add(id="reverse-words", title="Reverse Words in a String", difficulty="Medium", cat="two-pointers", tags=["String","Two Pointers"],
 desc=["Return the words of `s` in reverse order, separated by single spaces, with no leading or trailing spaces."],
 constraints=["1 <= s.length <= 10^4","s contains at least one word"], params=["s"], fn={"py":"reverse_words","js":"reverseWords"},
 examples=[["the sky is blue"],["  hello world  "],["a good   example"]], tests=[["the sky is blue"],["  hello world  "],["a good   example"],["one"],["  x  "]],
 hints=["Split into words (ignoring extra spaces), reverse the list, join with single spaces.","Without built-ins: reverse the whole string, then reverse each word."],
 editorial=["Splitting on whitespace discards the extra spaces; reversing the word list and joining with one space gives the answer. The in-place version (for mutable character arrays) reverses the whole string and then each word."],
 complexity="O(n) time.",
 py='''def reverse_words(s):
    return " ".join(reversed(s.split()))''',
 js='''function reverseWords(s) {
  return s.trim().split(/\\s+/).reverse().join(" ");
}''')

# ------------------------------------------------------------------ SLIDING WINDOW
add(id="max-average-subarray", title="Maximum Average Subarray", difficulty="Easy", cat="sliding-window", tags=["Array","Sliding Window"],
 desc=["Return the maximum average of any contiguous subarray of length exactly `k`."],
 constraints=["1 <= k <= nums.length <= 10^5"], params=["nums","k"], fn={"py":"find_max_average","js":"findMaxAverage"}, cmp="float",
 examples=[[[1,12,-5,-6,50,3],4],[[5],1]], tests=[[[1,12,-5,-6,50,3],4],[[5],1],[[0,4,0,3,2],1],[[-1,-2,-3],2],[rints(4000,-1000,1000),100]],
 hints=["Compute the first window's sum, then slide.","Sliding: add the new element, subtract the one leaving."],
 editorial=["A fixed-size window: maintain its sum in O(1) per step by adding the entering element and subtracting the leaving one. Track the best sum and divide by `k` once at the end."],
 complexity="O(n) time, O(1) space.",
 py='''def find_max_average(nums, k):
    window = best = sum(nums[:k])
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best / k''',
 js='''function findMaxAverage(nums, k) {
  let w = 0;
  for (let i = 0; i < k; i++) w += nums[i];
  let best = w;
  for (let i = k; i < nums.length; i++) { w += nums[i] - nums[i - k]; best = Math.max(best, w); }
  return best / k;
}''')

add(id="min-size-subarray-sum", title="Minimum Size Subarray Sum", difficulty="Medium", cat="sliding-window", tags=["Array","Sliding Window"],
 desc=["Given positive integers `nums` and a `target`, return the length of the shortest contiguous subarray whose sum is **at least** `target`, or 0 if none exists."],
 constraints=["1 <= nums.length <= 10^5","1 <= nums[i] <= 10^4"], params=["target","nums"], fn={"py":"min_sub_array_len","js":"minSubArrayLen"},
 examples=[[7,[2,3,1,2,4,3]],[4,[1,4,4]],[11,[1,1,1,1,1,1,1,1]]], tests=[[7,[2,3,1,2,4,3]],[4,[1,4,4]],[11,[1,1,1,1,1,1,1,1]],[15,[1,2,3,4,5]],[3,[1,1]],[100,rints(5000,1,50)]],
 hints=["All numbers are positive, so growing a window only increases its sum.","Grow on the right; while the sum is ≥ target, record the length and shrink from the left."],
 editorial=["Variable-size window: extend `right`, and while the window sum reaches the target, record its length and drop elements from the left. Positivity guarantees shrinking can only lower the sum, which is what makes this O(n)."],
 complexity="O(n) time, O(1) space.",
 py='''def min_sub_array_len(target, nums):
    best = float("inf")
    total = left = 0
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best''',
 js='''function minSubArrayLen(target, nums) {
  let best = Infinity, total = 0, left = 0;
  for (let r = 0; r < nums.length; r++) {
    total += nums[r];
    while (total >= target) { best = Math.min(best, r - left + 1); total -= nums[left++]; }
  }
  return best === Infinity ? 0 : best;
}''')

add(id="permutation-in-string", title="Permutation in String", difficulty="Medium", cat="sliding-window", tags=["String","Sliding Window","Hash Table"],
 desc=["Return `true` if `s2` contains a permutation of `s1` as a contiguous substring (an anagram of `s1` appears somewhere in `s2`)."],
 constraints=["1 <= s1.length, s2.length <= 10^4","lowercase English letters"], params=["s1","s2"], fn={"py":"check_inclusion","js":"checkInclusion"},
 examples=[["ab","eidbaooo"],["ab","eidboaoo"]], tests=[["ab","eidbaooo"],["ab","eidboaoo"],["a","a"],["abc","b"],["adc","dcda"],["hello","ooolleoooleh"]],
 hints=["A permutation has the same letter counts.","Slide a window of length `len(s1)` over `s2`, updating counts as it moves."],
 editorial=["Compare 26-letter count arrays for `s1` and the current window of `s2`. Sliding the window changes two counts, so each step is O(26)."],
 complexity="O(26 · n) time, O(1) space.",
 py='''def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    need = [0] * 26
    have = [0] * 26
    for ch in s1:
        need[ord(ch) - 97] += 1
    for i, ch in enumerate(s2):
        have[ord(ch) - 97] += 1
        if i >= len(s1):
            have[ord(s2[i - len(s1)]) - 97] -= 1
        if have == need:
            return True
    return False''',
 js='''function checkInclusion(s1, s2) {
  if (s1.length > s2.length) return false;
  const need = new Array(26).fill(0), have = new Array(26).fill(0);
  for (const c of s1) need[c.charCodeAt(0) - 97]++;
  for (let i = 0; i < s2.length; i++) {
    have[s2.charCodeAt(i) - 97]++;
    if (i >= s1.length) have[s2.charCodeAt(i - s1.length) - 97]--;
    if (need.every((v, j) => v === have[j])) return true;
  }
  return false;
}''')

# ------------------------------------------------------------------ STACK
add(id="backspace-compare", title="Backspace String Compare", difficulty="Easy", cat="stack", tags=["String","Stack"],
 desc=["In `s` and `t`, the character `#` means backspace. Return `true` if both strings end up equal after typing them into empty text editors."],
 constraints=["1 <= s.length, t.length <= 200"], params=["s","t"], fn={"py":"backspace_compare","js":"backspaceCompare"},
 examples=[["ab#c","ad#c"],["ab##","c#d#"],["a#c","b"]], tests=[["ab#c","ad#c"],["ab##","c#d#"],["a#c","b"],["#a","a"],["xy#z","xzz#"],["a##b","b"]],
 hints=["Simulate typing with a stack.","`#` pops (if the stack isn't empty); other characters push."],
 editorial=["Build the final text of each string with a stack (list): push characters, pop on `#`. Compare the results. An O(1)-space version walks both strings backwards counting skips."],
 complexity="O(n + m) time.",
 py='''def backspace_compare(s, t):
    def build(text):
        out = []
        for ch in text:
            if ch == "#":
                if out:
                    out.pop()
            else:
                out.append(ch)
        return out
    return build(s) == build(t)''',
 js='''function backspaceCompare(s, t) {
  const build = str => { const out = []; for (const c of str) c === "#" ? out.pop() : out.push(c); return out.join(""); };
  return build(s) === build(t);
}''')

add(id="simplify-path", title="Simplify Path", difficulty="Medium", cat="stack", tags=["String","Stack"],
 desc=["Simplify an absolute Unix path. `.` means the current directory, `..` means the parent (staying at `/` if already at the root), and repeated slashes count as one. Return the canonical path: it starts with `/`, has single slashes between names and no trailing slash."],
 constraints=["1 <= path.length <= 3000","path is absolute"], params=["path"], fn={"py":"simplify_path","js":"simplifyPath"},
 examples=[["/home/"],["/../"],["/home//foo/"],["/a/./b/../../c/"]], tests=[["/home/"],["/../"],["/home//foo/"],["/a/./b/../../c/"],["/a/../../b/../c//.//"],["/..."],["/"]],
 hints=["Split on `/` and handle each part.","A stack of directory names: push names, pop on `..`, ignore `.` and empty parts."],
 editorial=["Split by `/`. Empty parts and `.` do nothing; `..` pops if possible; anything else (including `...`, which is a valid name) pushes. Join the stack with `/` and prefix `/`."],
 complexity="O(n) time.",
 py='''def simplify_path(path):
    stack = []
    for part in path.split("/"):
        if part == "..":
            if stack:
                stack.pop()
        elif part and part != ".":
            stack.append(part)
    return "/" + "/".join(stack)''',
 js='''function simplifyPath(path) {
  const st = [];
  for (const p of path.split("/")) {
    if (p === "..") st.pop();
    else if (p && p !== ".") st.push(p);
  }
  return "/" + st.join("/");
}''')

add(id="next-greater-element", title="Next Greater Element", difficulty="Medium", cat="stack", tags=["Array","Monotonic Stack"],
 desc=["For each element of `nums`, return the first element to its right that is strictly greater, or `-1` if there isn't one."],
 constraints=["1 <= nums.length <= 10^5"], params=["nums"], fn={"py":"next_greater","js":"nextGreater"},
 examples=[[[2,1,2,4,3]],[[4,3,2,1]]], tests=[[[2,1,2,4,3]],[[4,3,2,1]],[[1]],[[1,2,3]],[[5,5,5]],[rints(3000,0,100)]],
 hints=["Brute force checks everything to the right: O(n²).","A stack of indexes still waiting for their answer, kept in decreasing value order."],
 editorial=["Scan left to right with a monotonic stack of indexes. When a new value is greater than the value at the top, it's the answer for that index: pop and record. Each index is pushed and popped once."],
 complexity="O(n) time, O(n) space.",
 py='''def next_greater(nums):
    ans = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        stack.append(i)
    return ans''',
 js='''function nextGreater(nums) {
  const ans = new Array(nums.length).fill(-1), st = [];
  nums.forEach((x, i) => {
    while (st.length && nums[st[st.length - 1]] < x) ans[st.pop()] = x;
    st.push(i);
  });
  return ans;
}''')

add(id="decode-string", title="Decode String", difficulty="Medium", cat="stack", tags=["String","Stack","Recursion"],
 desc=["Decode strings encoded as `k[text]`, meaning `text` repeated `k` times. Encodings can be nested, e.g. `3[a2[c]]` → `accaccacc`. Digits only appear as repeat counts."],
 constraints=["1 <= s.length <= 30","The input is always valid","1 <= k <= 300"], params=["s"], fn={"py":"decode_string","js":"decodeString"},
 examples=[["3[a]2[bc]"],["3[a2[c]]"],["2[abc]3[cd]ef"]], tests=[["3[a]2[bc]"],["3[a2[c]]"],["2[abc]3[cd]ef"],["abc"],["10[x]"],["2[a2[b2[c]]]"]],
 hints=["When you see `[`, you're starting a new nested string; remember what came before and the count.","Use a stack of (string so far, repeat count) pairs."],
 editorial=["Scan characters. Digits build up `k`. On `[` push the current string and `k`, then start fresh. On `]` pop the previous string and count and append `current * count`. Letters append to the current string."],
 complexity="O(output length).",
 py='''def decode_string(s):
    stack = []
    current, k = "", 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((current, k))
            current, k = "", 0
        elif ch == "]":
            prev, count = stack.pop()
            current = prev + current * count
        else:
            current += ch
    return current''',
 js='''function decodeString(s) {
  const st = [];
  let cur = "", k = 0;
  for (const c of s) {
    if (c >= "0" && c <= "9") k = k * 10 + Number(c);
    else if (c === "[") { st.push([cur, k]); cur = ""; k = 0; }
    else if (c === "]") { const [prev, n] = st.pop(); cur = prev + cur.repeat(n); }
    else cur += c;
  }
  return cur;
}''')

# ------------------------------------------------------------------ BINARY SEARCH
add(id="sqrt-x", title="Integer Square Root", difficulty="Easy", cat="binary-search", tags=["Math","Binary Search"],
 desc=["Return the square root of the non-negative integer `x`, rounded down, without using a built-in power or square-root function."],
 constraints=["0 <= x <= 2^31 - 1"], params=["x"], fn={"py":"my_sqrt","js":"mySqrt"},
 examples=[[4],[8]], tests=[[4],[8],[0],[1],[2],[15],[16],[2147395599],[2147483647]],
 hints=["The answer is the largest r with r × r ≤ x.","Binary search r in [0, x]."],
 editorial=["Binary search for the last `r` whose square is at most `x`. Using `mid * mid <= x` is safe in Python and in JavaScript at this size (the products stay below 2^53)."],
 complexity="O(log x) time.",
 py='''def my_sqrt(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo''',
 js='''function mySqrt(x) {
  let lo = 0, hi = x;
  while (lo < hi) {
    const mid = Math.floor((lo + hi + 1) / 2);
    if (mid * mid <= x) lo = mid; else hi = mid - 1;
  }
  return lo;
}''')

add(id="search-2d-matrix", title="Search a 2D Matrix", difficulty="Medium", cat="binary-search", tags=["Matrix","Binary Search"],
 desc=["Each row of `matrix` is sorted, and each row's first number is greater than the previous row's last. Return `true` if `target` is in the matrix, in O(log(m × n))."],
 constraints=["1 <= m, n <= 100"], params=["matrix","target"], fn={"py":"search_matrix","js":"searchMatrix"},
 examples=[[[[1,3,5,7],[10,11,16,20],[23,30,34,60]],3],[[[1,3,5,7],[10,11,16,20],[23,30,34,60]],13]], tests=[[[[1,3,5,7],[10,11,16,20],[23,30,34,60]],3],[[[1,3,5,7],[10,11,16,20],[23,30,34,60]],13],[[[1]],1],[[[1]],2],[[[1,3]],3],[[[1],[3]],3],[[[1,3,5,7],[10,11,16,20],[23,30,34,60]],60]],
 hints=["The matrix is really one sorted list laid out in rows.","Binary search over indexes 0..m·n−1, mapping index i to row i // n, column i % n."],
 editorial=["Treat the matrix as a flattened sorted array without building it: index `i` maps to `matrix[i // n][i % n]`. Standard binary search then runs in O(log(m·n))."],
 complexity="O(log(m × n)) time, O(1) space.",
 py='''def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // n][mid % n]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False''',
 js='''function searchMatrix(matrix, target) {
  const m = matrix.length, n = matrix[0].length;
  let lo = 0, hi = m * n - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1, v = matrix[Math.floor(mid / n)][mid % n];
    if (v === target) return true;
    if (v < target) lo = mid + 1; else hi = mid - 1;
  }
  return false;
}''')

add(id="find-peak-element", title="Find Peak Element", difficulty="Medium", cat="binary-search", tags=["Array","Binary Search"],
 desc=["A peak is an element strictly greater than its neighbours (outside the array counts as −∞). In these tests exactly one peak exists. Return its index in O(log n)."],
 constraints=["1 <= nums.length <= 1000","nums[i] != nums[i + 1]","exactly one peak in these tests"], params=["nums"], fn={"py":"find_peak_element","js":"findPeakElement"},
 examples=[[[1,2,3,1]],[[1,3,5,4,2]]], tests=[[[1,2,3,1]],[[1,3,5,4,2]],[[1]],[[2,1]],[[1,2]],[[1,2,3,4,5,6,7]],[[9,7,5,3]]],
 hints=["If `nums[mid] < nums[mid + 1]`, you're on an upward slope: a peak lies to the right.","Otherwise a peak is at `mid` or to its left."],
 editorial=["Binary search on the slope. Compare `mid` with `mid + 1`: rising means a peak exists to the right, falling means one exists at or left of `mid`. The range shrinks to the peak."],
 complexity="O(log n) time.",
 py='''def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo''',
 js='''function findPeakElement(nums) {
  let lo = 0, hi = nums.length - 1;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (nums[mid] < nums[mid + 1]) lo = mid + 1; else hi = mid; }
  return lo;
}''')
