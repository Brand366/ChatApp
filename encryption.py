#!/bin/bash

class Vigenere:
    '''
    Handles creating the key for the cipher and also the
    methods for encrypting and decrypting text with the cipher.

    Attributes:
        message (str): Message to be encrypted
        key (str): Key to use for encryption
    '''

    def __init__(self, message, key) -> None:
        self.message = message
        self.key = key

    def convert_message(self):
        '''
        Removes symbols and spaces from given message.
        '''
        self.message = self.message.upper()

        return ''.join(c for c in self.message if c.isalpha())

    def generate_key(self):
        '''
        Handles generating the key for encrypting and decrypting the given message.
        '''
        self.key = self.key.upper()

        return ''.join(self.key[char % len(self.key)]
                       for char in range(0, len(self.convert_message())))

    def encrypt(self):
        '''
        Handles encrypting the given message that has been converted to the appropriate
        format with the generated key.
        '''
        # stores the encrypted message result
        encrypted_message = []

        for index, letter in enumerate(self.convert_message()):
            # converts each letter in the given message and assigned indexed value
            # from the generated key to it's respective unicode value
            char_index = ord(letter)-65
            key_index = ord(self.generate_key()[index])-65
            # performs the modulo operation to shift each keyed value and
            # assign it the appropriate unicode value
            encrypted_char = chr(((char_index + key_index) % 26)+65)

            encrypted_message.append(encrypted_char)
        # converts the enrypted list into a string
        return ''.join(encrypted_message)

    def decrypt(self):
        '''
        Handles decrypting the encrypted message that has been converted to the appropriate
        format with the generated key.
        '''
        # stores the decrypted message result
        decrypted_message = []

        for index, letter in enumerate(self.encrypt()):
            # reverses the enryption operation for each keyed value
            key_index = ord(self.generate_key()[index])-65

            decrypted_char = chr((((ord(letter)-65)-key_index) % 26)+65)

            decrypted_message.append(decrypted_char)
        # converts the decrypted list into a string
        return ''.join(decrypted_message)
