
nums=[1,2,3,4,5,4,3,3,3,1,1]
k=2
count = {}
freq = [[] for i in range(len(nums) + 1)]
print(freq)
for n in nums:
    count[n] = 1 + count.get(n, 0)
for n, c in count.items():
    freq[c].append(n)
    
res = []
for i in range(len(freq) -1, 0, -1):
    for n in freq[i]:
        res.append(n)
    if len(res) == k:
        print(res)