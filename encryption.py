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

    def converted_message(self):
        '''
        Removes symbols and spaces from given message.
        '''
        converted_message = self.message.upper()
        converted_message = ''.join(
            c for c in converted_message if c.isalpha())
        return converted_message

    def generated_key(self):
        '''
        Handles generating the key for encrypting and decrypting the given message.
        '''
        self.key = ''.join(self.key[char % len(self.key)]
                           for char in range(len(self.converted_message())))
        return self.key

    def encrypt_text(self):
        encrypted_message = []

        for index, letter in enumerate(self.converted_message()):
            char_index = ord(letter)-65
            key_index = ord(self.generated_key()[index])-65

            encrypted_letter = chr(((char_index + key_index) % 26)+65)

            encrypted_message.append(encrypted_letter)

        return ''.join(encrypted_message)

    def decrypt_text(self):
        decrypted_message = []

        for index, letter in enumerate(self.encrypt_text()):
            key_index = ord(self.generated_key()[index])-65
            decrypted_char = chr((((ord(letter)-65)-key_index) % 26)+65)

            decrypted_message.append(decrypted_char)

        return ''.join(decrypted_message)
