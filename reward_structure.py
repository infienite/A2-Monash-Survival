from data_structures import ArrayMaxHeap, ArrayR, HashTableSeparateChaining


class UniqueArrayMaxHeap(ArrayMaxHeap):
    def __init__(self, max_items=1):
        """Initialize a unique max heap using array."""
        # Create index lookup for each element
        self._index_lookup = HashTableSeparateChaining(max_items)

        # Initialize from parent element
        super().__init__(max_items)

    def add(self, item):
        # Validate item
        self._validate_element(item)

        # Use parent class to add item
        super().add(item)

    def extract_root(self):
        # Get the max element
        res = super().extract_root()

        # Delete the max element lookup
        del self._index_lookup[str(res)]

        # Return max element
        return res

    def _rise(self, k):
        # Element heap array
        rising_item = self._array[k]

        # Rise element if element is larger than its parent until reaches correct position
        while k > 1 and rising_item > self._array[k // 2]:
            self._array[k] = self._array[k // 2]
            self._index_lookup[str(self._array[k // 2])] = k
            k = k // 2

        # Update element and index lookup
        self._array[k] = rising_item
        self._index_lookup[str(rising_item)] = k

    def _sink(self, k):
        sinking_item = self._array[k]

        # Sink element if element is smaller than its child until reaches correct position
        while 2 * k <= len(self):
            child_i = self._get_child_index(k)
            if sinking_item >= self._array[child_i]:
                break
            self._array[k] = self._array[child_i]
            self._index_lookup[str(self._array[child_i])] = k
            k = child_i

        # Update element and index lookup
        self._array[k] = sinking_item
        self._index_lookup[str(sinking_item)] = k

    @classmethod
    def heapify(cls, from_array: ArrayR, min_capacity=1):
        """Use bottom-up heap construction to build the heap."""
        # Get length of array
        length = len(from_array)
        if min_capacity > length:
            length = min_capacity

        # Initialize heap array and lookup table
        array = ArrayR(length + 1)
        index_lookup = HashTableSeparateChaining(length)

        # Copy the array into heap array but leave index 0 empty and store all lookups
        for i in range(length):
            array[i + 1] = from_array[i]
            index_lookup.insert(str(from_array[i]), i + 1)
            i += 1

        # Duplicate exists if the lookup contains less key than the number of element of array
        if len(index_lookup.keys()) != length:
            raise ValueError("Cannot contain duplicate elements in unique heap")

        # Initialize unique heap
        heap = cls(length)

        # Assign heap array and lookup table
        heap._array = array
        heap._index_lookup = index_lookup
        heap._length = length

        # Build the heap bottom-up construction
        for i in range(len(heap) // 2, 0, -1):
            heap._sink(i)

        # Return the heap
        return heap

    def update(self, elem, new_elem):
        """Update the element to a new value."""

        # Halts early if the current element is the same as the new element
        if elem == new_elem:
            return

        # Validate argument
        self._validate_element(new_elem)

        # Update the element at that index
        k = self._index_lookup[str(elem)]
        self._array[k] = new_elem

        # Rise when new element is larger than the previous value
        if new_elem > elem:
            self._rise(k)

        # Sink when new element is smaller than the previous value
        elif new_elem < elem:
            self._sink(k)

        # Delete the old index lookup to the element with the previous value
        del self._index_lookup[str(elem)]

    def _is_unique(self, elem) -> bool:
        """Return true if element is not inside the heap."""
        # Index is not unique if it already exist inside the hash table
        try:
            _ = self._index_lookup[str(elem)]
            return False

        # Index is unique if it's not inside hash table
        except KeyError:
            return True

    def _validate_element(self, elem):
        """Raise error if element already exists."""
        if not self._is_unique(elem):
            raise ValueError(f"The element {str(elem)} already exists inside the heap.")
