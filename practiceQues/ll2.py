class Solution():
    def countBits(self, num):
        if num == 0:
             return [0]
        dp = []
        dp.append(0)
        dp.append(1)
        for i in range(2, num+1):
            if i%2 == 0: 
                dp.append(dp[int(i/2)])
            else: 
                dp.append(1 + dp[int((i-1)/2)])
                
        return dp

obj=Solution()
print(obj.countBits(8))