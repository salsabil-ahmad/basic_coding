# finding peak of a mountain array

def binarySearch(arr):
    high = len(arr)-1
    low = 0
    while high >= low:
        mid = low + (high - low)/2
        mid=int(mid)

        if low==high:
            return low

        elif arr[mid] < arr[mid+1]:
            low = mid + 1
            
        else:
            high = mid

    # return low

            
arr = [1,2,4,5,7,9,6,4,3,2]
print(binarySearch(arr))

