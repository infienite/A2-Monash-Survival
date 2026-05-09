from data_structures import ArrayR, HashTableSeparateChaining

class ArrayMaxHeap(ArrayR):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int, an_array: ArrayR = None, verbose=False) -> None:
        """
        If an_array is specified then the elements of the future 
        heap are known in advance.
        Assume that max_size=len(an_array) if given.
        """

        # playing with the arguments to set up the length
        if an_array is None:
            self._length = 0 # missing on page 126 of 20-Heaps2.pdf
        else:
            self._length = max_size = len(an_array) 
        
        # allocate the array
        self._the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)
        
        self.lookup = HashTableSeparateChaining(self._length)
        
        # if an_array is given then apply bottom-up heap construction
        if an_array:
            self.heapify(an_array, verbose)


    def __len__(self) -> int:
        return self._length

    def is_full(self) -> bool:
        return self._length + 1 == len(self._the_array)

    def heapify(self, an_array: ArrayR, verbose=False) -> None:
        """
        Apply bottom-up heap construction in O(n) time.
        """

        # copy an_array to self._the_array (shift by 1)
        for i in range(self._length):
            self._the_array[i + 1] = an_array[i]
            self.lookup[str(an_array[i])] = i + 1

        if verbose:
            print('the_array before bottom-up heap construction')
            for i in self._the_array:
                print(i)

        # heapify every parent
        for i in range(self._length // 2, 0, -1):
            if verbose:
                print('sinking the parent', i)

            k = self.sink(i)

            if verbose:
                for i in self._the_array:
                    print(i)

        if verbose:
            print('the_array after bottom-up heap construction')
            for i in self._the_array:
                print(i)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self._length
        """
        item = self._the_array[k]

        while k > 1 and item > self._the_array[k // 2]:
            self._the_array[k] = self._the_array[k // 2]
            self.lookup[str(self._the_array[k // 2])] = k
            k = k // 2
        self._the_array[k] = item
        self.lookup[str(item)] = k

    def add(self, element) -> bool:
        """
        Swaps elements while rising
        """
        if self.is_full():
            raise IndexError

        self._length += 1
        self._the_array[self._length] = element
        self.rise(self._length)

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.
        :pre: 1 <= k <= self._length // 2
        """
        
        if 2 * k == self._length or \
                self._the_array[2 * k] > self._the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position.
            :pre: 1 <= k <= self._length
            :complexity: ???
        """
        item = self._the_array[k]

        while 2 * k <= self._length:
            max_child = self.largest_child(k)
            if self._the_array[max_child] <= item:
                break
            self._the_array[k] = self._the_array[max_child]
            self.lookup[str(self._the_array[max_child])] = k
            k = max_child

        self._the_array[k] = item
        self.lookup[str(item)] = k
        return k
        
    def get_max(self):
        """ Remove (and return) the maximum element from the heap. """
        if self._length == 0:
            raise IndexError

        max_elt = self._the_array[1]
        del self.lookup[str(max_elt)]
        self._length -= 1
        if self._length > 0:
            self._the_array[1] = self._the_array[self._length+1]
            self.sink(1)
        return max_elt
    
    def update(self, elem, new_elem):
        # print(self.lookup.keys())
        k = self.lookup[str(elem)]
        self._the_array[k] = new_elem

        if elem == new_elem:
            return
        if new_elem > elem:
            self.rise(k)
        elif new_elem < elem:
            self.sink(k)
        del self.lookup[str(elem)]

if __name__ == '__main__':
    #items = [ int(x) for x in input('Enter a list of numbers: ').strip().split() ]
    items = [ 1, 9, 12, 5, 17, 15, 2]
    heap = ArrayMaxHeap(len(items), items)
    
    for i in heap._the_array:
        print("Item", i)

    print()

    # output all elements of the heap in descending order
    while(len(heap) > 0):
        print(heap.get_max())