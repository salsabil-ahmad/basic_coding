def binarySearch(arr, key):
    high = len(arr)-1
    low = 0
    while high >= low:
        mid = low + (high - low)/2
        mid=int(mid)
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            high = mid - 1
        else :
            low = mid + 1
    return -1

arr = ["a","c","f","i","l"]
key = "m"
print(binarySearch(arr,key))

