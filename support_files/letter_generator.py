class LetterCycler:
    """
    A class that generates a sequence of letters similar to Excel column names:
    A, B, C, ..., Z, AA, AB, ..., AZ, BA, ..., ZZ, AAA, etc.
    Stores all generated sequences in a history list.
    """
    
    def __init__(self):
        # _current_chars stores the individual characters of the *next* letter sequence
        # to be generated (e.g., ['A', 'A'] for "AA"). It's initialized empty,
        self._current_chars = []
        # _generated_history stores all *completed* letter sequences as strings,
        # appended each time next_letter() is called.
        self._generated_history = []

    def next_letter(self):
        """
        Generates and returns the next letter in the sequence.
        This method also appends the newly generated letter to an internal history list.

        Returns:
            str: The next letter sequence (e.g., "A", "B", "AA", "AB").
        """
        # If _current_chars is empty, initialize the sequence with 'A'.
        if not self._current_chars:
            self._current_chars = ['A']
        else:
            # Iterate through the characters from right to left (end to beginning).
            i = len(self._current_chars) - 1
            while i >= 0:
                current_char_code = ord(self._current_chars[i])

                # If the current character is 'Z', it "overflows".
                # Reset it to 'A' and continue to the next position (left) to carry.
                if current_char_code == ord('Z'):
                    self._current_chars[i] = 'A'
                    i -= 1 # Move left to propagate the carry
                else:
                    # If not 'Z', increment the character by one.
                    self._current_chars[i] = chr(current_char_code + 1)
                    break # Increment successful, stop carrying

            # If the loop finished and 'i' is less than 0, it means all characters
            # were 'Z' and wrapped around (e.g., 'Z' became 'A', 'AZ' became 'AA', 'ZZ' became 'AAA').
            if i < 0:
                self._current_chars.insert(0, 'A')

        # Convert the list of characters into a single string for the current sequence.
        current_sequence_str = "".join(self._current_chars)
        
        # Append the newly generated sequence to the history list.
        self._generated_history.append(current_sequence_str)
        
        # Return the newly generated sequence.
        return current_sequence_str

    def get_history(self):
        """
        Returns a list of all letter sequences generated so far.

        Returns:
            list: A list of strings, where each string is a generated letter sequence.
        """
        return self._generated_history

    def get_last_generated(self):
        """
        Returns the last letter sequence generated from the history.

        Returns:
            str or None: The last generated letter sequence, or None if no sequences have been generated yet.
        """
        if not self._generated_history:
            return None
        return self._generated_history[-1]
