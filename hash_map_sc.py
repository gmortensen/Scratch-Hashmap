# Name: Gabriel Mortensen
# OSU Email: mortenga@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation with Chaining Collision Resolution
# Due Date: 06/03/2022
# Description: Implementation of a HashMap using a Dynamic Array to store the Hash Table and chaining for collision
# resolution using a singly-linked list. Chains of Key/Value pairs are stored in the nodes of the Linked List.
# Implementation includes put, get, remove, contains_key, clear, empty_buckets, resize_table, table_load, get_keys,
# and find_mode methods.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        This method updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a key / value pair must be added.
        """
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].contains(key) is False or self._buckets[index].contains(key) is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value
                    return

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        num_buckets = 0
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket]._head is None:
                num_buckets += 1
        return num_buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        curr_capacity = self._capacity
        self._buckets = DynamicArray()
        self._size = 0
        for bucket in range(curr_capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed. If
        new_capacity is less than 1, the method does nothing.
        """
        if new_capacity < 1:
            return
        new_map = HashMap(new_capacity, self._hash_function)
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket]._head is not None:
                for node in self._buckets[bucket]:
                    new_map.put(node.key, node.value)
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
        if self._buckets[index]._head is not None:
            for node in self._buckets[index]:
                if node.key == key:
                    return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        if self._size == 0:
            return False
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index]._head is not None:
            for node in self._buckets[index]:
                if node.key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing
        """
        if self._size == 0:
            return
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index]._head is not None:
            result = self._buckets[index].remove(key)
            if result is True:
                self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map
        """
        all_keys = DynamicArray()
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket]._head is not None:
                for node in self._buckets[bucket]:
                    all_keys.append(node.key)
        return all_keys

    def mode_put(self, key: str) -> None:
        """
        This method updates the key / value pair in a hash map used to find the mode value of a dynamic array.
        The key is the object or string from the dynamic array, and the value is the number of times the key appears
        in the original dynamic array.
        """
        index = self._hash_function(key) % self.get_capacity()
        new_key_val = 1
        if self._buckets[index].contains(key) is False or self._buckets[index].contains(key) is None:
            self._buckets[index].insert(key, new_key_val)
            self._size += 1
        else:
            for node in self._buckets[index]:
                if node.key == key:
                    node.value += 1
                    return


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function will return a tuple containing, in this order, a DynamicArray comprising the mode (most occurring)
    values of the array, and an integer that represents the highest frequency. If there is more than one value with
    the highest frequency, all values at that frequency should be included in the array being returned (the order
    does not matter). If there is only one mode, return a DynamicArray comprised of only that value.
    """
    map = HashMap(da.length() // 3, hash_function_1)
    for i in range(da.length()):
        map.mode_put(da[i])         # adds key/value pair to a HashMap with value holding number of times a key appears
    mode_count = 0
    keys_arr = map.get_keys()
    for key in range(keys_arr.length()):
        value = map.get(keys_arr[key])
        if value is not None and value > mode_count:
            mode_count = value
    mode_arr = DynamicArray()
    for key in range(keys_arr.length()):
        value = map.get(keys_arr[key])
        if value == mode_count:
            mode_arr.append(keys_arr[key])
    return (mode_arr, mode_count)

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
