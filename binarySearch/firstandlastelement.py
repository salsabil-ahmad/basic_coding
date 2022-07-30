def findinglist(arr,key):
    ans=[-1,-1]
    ans[0]=binarySearch(arr, key, False, -1)
    ans[1]=binarySearch(arr, key, True, -1)
    return ans

def binarySearch(arr, key, position, ans):
    high = len(arr)-1
    low = 0
    while high >= low:
        mid = low + (high - low)/2
        mid=int(mid)
        if arr[mid] < key:
            low = mid + 1
            
        elif arr[mid] > key:
            high = mid - 1
        else :
            ans = mid
            if position == False:
                high=mid-1
            else:
                low=mid+1
    return ans

arr = [1,2,3,4,5,7,8,10,10,10,10,11]
key = 10
print(findinglist(arr,key))
