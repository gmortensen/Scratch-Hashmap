# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)
        index = self._hash_function(key) % self.get_capacity()
        new_entry = HashEntry(key, value)
        if self._buckets[index] is None:
            self._buckets[index] = new_entry
            self._size += 1
            return
        # Target index is not empty. Check if index key is the same as new key, update value if it is
        if self.key_exists(self._buckets[index], new_entry) is True:
            return
        quad_probe = 1
        start_index = index
        while self._buckets[index] is not None:
            index = (start_index + quad_probe**2) % self.get_capacity()
            quad_probe += 1
            if self.key_exists(self._buckets[index], new_entry) is True:
                return
        self._buckets[index] = new_entry
        self._size += 1
        return

    def key_exists(self, old_entry, new_entry):
        if old_entry is None:
            return False
        if old_entry.key == new_entry.key:
            old_entry.value = new_entry.value
            if old_entry.is_tombstone is True:
                old_entry.is_tombstone = False
                self._size += 1
            return True
        return False

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """

        """
        num_buckets = 0
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket] is None or self._buckets[bucket].is_tombstone is True:
                num_buckets += 1
        return num_buckets

    def resize_table(self, new_capacity: int) -> None:
        """

        """
        # remember to rehash non-deleted entries into new table
        # Come back and add tests and functionality to ensure that tombstone values are not being included
        # in the new resized table. If a value from the old table was a Tombstone value, it should not count towards
        # size
        if new_capacity < 1 or new_capacity < self._size:
            return
        new_map = HashMap(new_capacity, self._hash_function)
        new_map._capacity = new_capacity
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket] is not None and self._buckets[bucket].is_tombstone is False:
                new_map.put(self._buckets[bucket].key, self._buckets[bucket].value)
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity
        self._hash_function = new_map._hash_function
        self._size = new_map._size

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        index = self._hash_function(key) % self.get_capacity()
        if self._size == 0 or self._buckets[index] is None:
            return None
        if self._buckets[index].is_tombstone is True and self._buckets[index].key == key:  # checks if key has been
            return None  # removed from the hashmap
        if self._buckets[index].key == key:
            return self._buckets[index].value
        if self._buckets[index].key != key:
            quad_probe = 1
            start_index = index
            while self._buckets[index] is not None:
                index = (start_index + quad_probe ** 2) % self.get_capacity()
                if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                    return None
                if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                    return self._buckets[index].value
                quad_probe += 1
            return None


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        index = self._hash_function(key) % self.get_capacity()
        if self._size == 0 or self._buckets[index] is None:
            return False
        if self._buckets[index].is_tombstone is True and self._buckets[index].key == key:   # checks if key has been
            return False                                                                    # removed from the hashmap
        if self._buckets[index].key == key:
            return True
        if self._buckets[index].key != key:
            quad_probe = 1
            start_index = index
            while self._buckets[index] is not None:
                index = (start_index + quad_probe ** 2) % self.get_capacity()
                if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                    return False
                if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                    return True
                quad_probe += 1
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """

        index = self._hash_function(key) % self.get_capacity()
        if self._size == 0 or self._buckets[index] is None:
            return
        if self._buckets[index].is_tombstone is True and self._buckets[index].key == key:
            return
        if self._buckets[index].key == key:
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return
        if self._buckets[index].key != key:
            quad_probe = 1
            start_index = index
            while self._buckets[index] is not None:
                index = (start_index + quad_probe ** 2) % self.get_capacity()
                if self._buckets[index] is None:
                    return
                if self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
                    return
                if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return
                quad_probe += 1
            return

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        curr_capacity = self._capacity
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(curr_capacity):
            self._buckets.append(None)

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map.
        """
        all_keys = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone is False:
                    all_keys.append(self._buckets[i].key)
        return all_keys

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
