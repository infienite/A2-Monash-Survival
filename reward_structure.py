from data_structures import ArrayR, HashTableSeparateChaining


class UniqueArrayMaxHeap:
    _MIN_CAPACITY = 1

    def __init__(self, max_size: int, initial_heap_elements: ArrayR = None) -> None:
        """ Initialize a unique max heap using array. Applies bottom-up construction to fill with element inside array or start with empty heap if no array provided. """
        # Initialize the empty array heap
        self._heap_array = ArrayR(max(self._MIN_CAPACITY, max_size) + 1)
        
        # Hash table to track element index inside the array
        self._index_lookup = HashTableSeparateChaining(max(self._MIN_CAPACITY, max_size))
        
        # When no array provided, keep empty heap
        if initial_heap_elements is None:
            self._length = 0
            return
        
        # Heapify the array using bottom-up construction
        self._length = len(initial_heap_elements)
        self._heapify(initial_heap_elements)

    def _is_unique(self, elem) -> bool:
        """ Return true if element is not inside the heap. """
        # Index is not unique if it already exist inside the hash table
        try:
            _ = self._index_lookup[str(elem)]
            return False
        
        # Index is unique if it's not inside hash table
        except KeyError:
            return True
        
    def _validate_element(self, elem):
        """ Raise error if element already exists. """
        if not self._is_unique(elem):
            raise ValueError(f'The element {str(elem)} already exists inside the heap.')
    
    def __len__(self) -> int:
        """ Return number of element inside heap array. """
        return self._length

    def is_full(self) -> bool:
        """ Checks if the number of element has reached maximum capacity of the heap. """
        return self._length + 1 == len(self._heap_array)

    def _heapify(self, from_array: ArrayR) -> None:
        """ Use bottom-up heap construction to build the heap. """
        # Copy the array into heap array but leave index 0 empty
        for i in range(self._length):
            self._validate_element(from_array[i])
            self._heap_array[i + 1] = from_array[i]
            self._index_lookup[str(from_array[i])] = i + 1

        # Heapify parents of the tree
        for i in range(self._length // 2, 0, -1):
            self._sink(i)

    def _rise(self, k: int) -> None:
        """ Rise element at index k to its correct position. """
        # Element heap array
        elem = self._heap_array[k]

        # Rise element if element is larger than its parent until reaches correct position
        while k > 1 and elem > self._heap_array[k // 2]:
            self._heap_array[k] = self._heap_array[k // 2]
            self._index_lookup[str(self._heap_array[k // 2])] = k
            k = k // 2
        
        # Update element and index lookup
        self._heap_array[k] = elem
        self._index_lookup[str(elem)] = k

    def add(self, element) -> bool:
        """ Swaps elements while rising. """
        # Cannot add more element when tree is full
        if self.is_full():
            raise IndexError
        
        # Validate element
        self._validate_element(element)

        # Update length and insert new element at end of array
        self._length += 1
        self._heap_array[self._length] = element
        
        # Rise the new element to the correct position
        self._rise(self._length)

    def _largest_child(self, k: int) -> int:
        """ Returns the index of k's child with greatest value. """
        if 2 * k == self._length or \
                self._heap_array[2 * k] > self._heap_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def _sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position. """
        item = self._heap_array[k]

        # Sink element if element is smaller than its child until reaches correct position
        while 2 * k <= self._length:
            max_child = self._largest_child(k)
            if self._heap_array[max_child] <= item:
                break
            self._heap_array[k] = self._heap_array[max_child]
            self._index_lookup[str(self._heap_array[max_child])] = k
            k = max_child

        # Update element and index lookup
        self._heap_array[k] = item
        self._index_lookup[str(item)] = k
        
    def get_max(self):
        """ Remove (and return) the maximum element from the heap. """
        # Cannot get max element when there is no element
        if self._length == 0:
            raise IndexError

        # Get maximum element of heap
        max_elem = self._heap_array[1]

        # Delete the index lookup of element
        del self._index_lookup[str(max_elem)]

        # Update length
        self._length -= 1

        # Ensure max element at the top by sinking the element if it's lower than its child
        if self._length > 0:
            self._heap_array[1] = self._heap_array[self._length+1]
            self._sink(1)
        
        # Return max element
        return max_elem
    
    def update(self, elem, new_elem):
        """ Update the element to a new value. """

        # Halts early if the current element is the same as the new element
        if elem == new_elem:
            return

        # Validate argument
        self._validate_element(new_elem)

        # Update the element at that index
        k = self._index_lookup[str(elem)]
        self._heap_array[k] = new_elem
        
        # Rise when new element is larger than the previous value
        if new_elem > elem:
            self._rise(k)
        
        # Sink when new element is smaller than the previous value
        elif new_elem < elem:
            self._sink(k)
        
        # Delete the old index lookup to the element with the previous value
        del self._index_lookup[str(elem)]


if __name__ == '__main__':
    #items = [ int(x) for x in input('Enter a list of numbers: ').strip().split() ]
    items = [ 1, 9, 12, 5, 17, 15, 2]
    max_heap = UniqueArrayMaxHeap(len(items), items)

    print(max_heap.get_max())

    max_heap.update(5, 19)

    print(max_heap.get_max())

    max_heap.update(12, 20)
    max_heap.update(9, 21)
    max_heap.update(1, 22)
    max_heap.update(2, 24)

    print(max_heap.get_max())
    print(max_heap.get_max())
    print(max_heap.get_max())
    print(max_heap.get_max())
    
    max_heap.add(4)

    max_heap.update(4, 200)
    print(max_heap.get_max())
    print(max_heap.get_max())
