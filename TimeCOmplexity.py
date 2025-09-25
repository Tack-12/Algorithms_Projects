def bubbleSort(arr):
    n= len(arr)

    for i in range(n):
        sorted= False

        for j in range(0,n-i-1):
            if (arr[j]>arr[j+1]):
                arr[j],arr[j+1]=arr[j+1],arr[j]
                sorted= True

        if(sorted==True):
            break
        
def mergeSort(arr):





def quickSort(arr):