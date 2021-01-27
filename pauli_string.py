"""
pauli_string.py - Define PauliString and LinearCombinaisonPauliString

Copyright 2020-2021 Maxime Dion <maxime.dion@usherbrooke.ca>
This file has been modified by <Your,Name> during the
QSciTech-QuantumBC virtual workshop on gate-based quantum computing.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np


class PauliString(object):

    def __init__(self, z_bits, x_bits):
        """
        Describe a Pauli string as 2 arrays of booleans.
        The PauliString represents (-1j)**(z_bits*x_bits) Z**z_bits X**x_bits.

        Args:
            z_bits (np.ndarray<bool>): True where a Z Pauli is applied.
            x_bits (np.ndarray<bool>): True where a X Pauli is applied.

        Raises:
            ValueError: [description]
        """

        if len(z_bits) != len(x_bits):
            raise ValueError('z_bits and x_bits must have the same number of elements')
        self.z_bits = z_bits
        self.x_bits = x_bits

    def __str__(self):
        """
        String representation of the PauliString.

        Returns:
            str: String of I, Z, X and Y.
        """

        pauli_labels = 'IZXY'
        pauli_choices = (self.z_bits + 2*self.x_bits).astype(int)
        out = ''
        for i in reversed(pauli_choices):
            out += pauli_labels[i]
        return out

    def __len__(self):
        """
        Number of Pauli in the PauliString.
        Also the number of qubits.

        Returns:
            int: Length of the PauliString, also number of qubits.
        """

        return len(self.z_bits)

    def __mul__(self, other):
        """
        Allow the use of '*' with other PauliString or with a coef (numeric).

        Args:
            other (PauliString): Will compute the product 
            or
            other (float): [description]

        Returns:
            PauliString, complex: When other is a PauliString
            or
            LinearCombinaisonPauliString : When other is numeric
        """
        if isinstance(other,PauliString):
            return self.mul_pauli_string(other)
        else:
            return self.mul_coef(other)

    def __rmul__(self, other):
        """
        Same as __mul__. Allow the use of '*' with a preceding coef (numeric) Like in 0.5 * PauliString

        Args:
            other (PauliString): Will compute the product 
            or
            other (float): [description]

        Returns:
            PauliString, complex: When other is a PauliString
            or
            LinearCombinaisonPauliString : When other is numeric
        """

        return self.__mul__(other)

    @classmethod
    def from_zx_bits(cls, zx_bits):
        """
        Construct a PauliString from a single array<bool> of len 2n.

        Args:
            zx_bits (np.array<bool>): An array of bools. First n bits specify the Zs. Second half specify the Xs.

        Returns:
            PauliString: The Pauli string specified by the 'zx_bits'.
        """

        z_bits = x_bits = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        z_bits = zx_bits[:len(zx_bits)//2]
        x_bits = zx_bits[len(zx_bits)//2:]
        ################################################################################################################
        
        return cls(z_bits, x_bits)

    @classmethod
    def from_str(cls, pauli_str):
        """
        Construct a PauliString from a str (as returned by __str__).

        Args:
            pauli_str (str): String of length n made of 'I', 'X', 'Y' and 'Z'.

        Returns:
            PauliString: The Pauli string specified by the 'pauli_str'.
        """

        z_bits, x_bits = [], []

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        for pauli in pauli_str[::-1]:
            if pauli.upper() == 'X':
                z_bits.append(False)
                x_bits.append(True)
            elif pauli.upper() == 'Y':
                z_bits.append(True)
                x_bits.append(True)
            elif pauli.upper() == 'Z':
                z_bits.append(True)
                x_bits.append(False)
            elif pauli.upper() == 'I':
                z_bits.append(False)
                x_bits.append(False)
            else:
                raise ValueError('Pauli string must only have characters X, Y, Z, and I')
        
        z_bits = np.array(z_bits, dtype=bool)
        x_bits = np.array(x_bits, dtype=bool)
        
        return cls(z_bits, x_bits)

    def to_zx_bits(self):
        """
        Return the zx_bits representation of the PauliString.
        Useful to compare PauliString together.

        Returns:
            np.array<bool>: zx_bits representation of the PauliString of length 2n
        """

        zx_bits = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        
        zx_bits = np.concatenate((self.z_bits, self.x_bits))

        return zx_bits

    def to_xz_bits(self):
        """
        Return the xz_bits representation of the PauliString.
        Useful to check commutativity.

        Returns:
            np.array<bool>: xz_bits representation of the PauliString of length 2n
        """

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        
        xz_bits = np.concatenate((self.x_bits, self.z_bits))

        return xz_bits

    def mul_pauli_string(self, other):
        """
        Product with an 'other' PauliString.

        Args:
            other (PauliString): An other PauliString.

        Raises:
            ValueError: If the other PauliString is not of the same length.

        Returns:
            PauliString, complex: The resulting PauliString and the product phase.
        """
        
        if len(self) != len(other):
            raise ValueError('PauliString must be of the same length')

        new_z_bits = new_x_bits = phase = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        # xor will do mod 2 addition to the bitstring
        new_z_bits = np.logical_xor(self.z_bits, other.z_bits)
        new_x_bits = np.logical_xor(self.x_bits, other.x_bits)
        # 2z2 · x1 + z1 · x1 + z2 · x2 - z3 · x3
        w = (2 * np.sum(np.logical_and(other.z_bits, self.x_bits)) 
             + np.sum(np.logical_and(self.z_bits, self.x_bits)) 
             + np.sum(np.logical_and(other.z_bits, other.x_bits)) 
             - np.sum(np.logical_and(new_z_bits, new_x_bits))) % 4 
        phase = (-1j)**w
        ################################################################################################################
        
        return self.__class__(new_z_bits, new_x_bits), phase

    def mul_coef(self, coef):
        """
        Build a LCPS from a PauliString (self) and a numeric (coef).

        Args:
            coef (int, float or complex): A numeric coefficient.

        Returns:
            LinearCombinaisonPauliString: A LCPS with only one PauliString and coef.
        """

        coefs = pauli_strings = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        coefs = np.array([coef], dtype=complex)
        pauli_strings = np.array([self], dtype=PauliString)
        ################################################################################################################

        return LinearCombinaisonPauliString(coefs, pauli_strings)

    def ids(self):
        """
        Position of Identity in the PauliString.

        Returns:
            np.array<bool>: True where both z_bits and x_bits are False.
        """

        ids = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################

        ids = (self.x_bits | self.z_bits) == False

        return ids

    def copy(self):
        """
        Build a copy of the PauliString.

        Returns:
            PauliString: A copy.
        """

        return PauliString(self.z_bits.copy(), self.x_bits.copy())

    def to_matrix(self):
        """
        Build the matrix representation of the PauliString using the Kroenecker product.

        Returns:
            np.array<complex>: A 2**n side square matrix.
        """

        I_MAT = np.array([[1, 0],[0, 1]])
        X_MAT = np.array([[0, 1],[1, 0]])
        Y_MAT = np.array([[0, -1j],[1j, 0]])
        Z_MAT = np.array([[1, 0],[0, -1]])

        matrix = None

        ################################################################################################################
        # YOUR CODE HERE (OPTIONAL)
        # TO COMPLETE (after activity 3.1)
        # Hints : start with
        # matrix = np.ones((1,1),dtype = np.complex)
        # And then use the np.kron() method to build the matrix
        ################################################################################################################

        paulis = [I_MAT, Z_MAT, X_MAT, Y_MAT]
        matrix = np.ones((1,1),dtype = np.complex)
        
        for pauli in reversed((self.z_bits + 2*self.x_bits).astype(int)):   
            matrix = np.kron(matrix, paulis[pauli])
        
        return matrix


class LinearCombinaisonPauliString(object):
    def __init__(self,coefs,pauli_strings):
        """
        Describes a Linear Combinaison of Pauli Strings.

        Args:
            coefs (np.array): Coefficients multiplying the respective PauliStrings.
            pauli_strings (np.array<PauliString>): PauliStrings.

        Raises:
            ValueError: If the number of coefs is different from the number of PauliStrings.
            ValueError: If all PauliStrings are not of the same length.
        """

        if len(coefs) != len(pauli_strings):
            raise ValueError('Must provide a equal number of coefs and PauliString')

        n_qubits = len(pauli_strings[0])
        for pauli in pauli_strings:
            if len(pauli) != n_qubits:
                raise ValueError('All PauliString must be of same length')

        self.n_terms = len(pauli_strings)
        self.n_qubits = len(pauli_strings[0])

        self.coefs = np.array(coefs, dtype=complex)
        self.pauli_strings = np.array(pauli_strings, dtype=PauliString)
        
    def __str__(self):
        """
        String representation of the LinearCombinaisonPauliString.

        Returns:
            str: Descriptive string.
        """

        out = f'{self.n_terms:d} pauli strings for {self.n_qubits:d} qubits (Real, Imaginary)'
        for coef, pauli in zip(self.coefs,self.pauli_strings):
            out += '\n' + f'{str(pauli)} ({np.real(coef):+.5f},{np.imag(coef):+.5f})'
        return out

    def __getitem__(self, key):
        """
        Return a subset of the LinearCombinaisonPauliString array-like.

        Args:
            key (int or slice): Elements to be returned.

        Returns:
            LinearCombinaisonPauliString: LCPS with the element specified in key.
        """
        
        if isinstance(key,slice):
            new_coefs = np.array(self.coefs[key])
            new_pauli_strings = self.pauli_strings[key]
        else:
            if isinstance(key,int):
                key = [key]
            new_coefs = self.coefs[key]
            new_pauli_strings = self.pauli_strings[key]

        return self.__class__(new_coefs,new_pauli_strings)

    def __len__(self):
        """
        Number of PauliStrings in the LCPS.

        Returns:
            int: Number of PauliStrings/coefs.
        """

        return len(self.pauli_strings)

    def __add__(self,other):
        """
        Allow the use of + to add two LCPS together.

        Args:
            other (LinearCombinaisonPauliString): An other LCPS.

        Returns:
            LinearCombinaisonPauliString: New LCPS of len = len(self) + len(other).
        """

        return self.add_pauli_string_linear_combinaison(other)

    def __mul__(self, other):
        """
        Allow the use of * with other LCPS or numeric value(s)

        Args:
            other (LinearCombinaisonPauliString): An other LCPS

        Returns:
            LinearCombinaisonPauliString: New LCPS of len = len(self) * len(other)
            or
            LinearCombinaisonPauliString: New LCPS of same length with modified coefs
        """
        
        if isinstance(other,LinearCombinaisonPauliString):
            return self.mul_linear_combinaison_pauli_string(other)
        else:
            return self.mul_coef(other)

    def __rmul__(self, other):
        """
        Same as __mul__.
        Allow the use of '*' with a preceding coef (numeric).
        Like in 0.5 * LCPS.

        Args:
            other (LinearCombinaisonPauliString): An other LCPS.

        Returns:
            LinearCombinaisonPauliString: New LCPS of len = len(self) * len(other)
            or
            LinearCombinaisonPauliString: New LCPS of same length with modified coefs
        """
        
        return self.__mul__(other)

    def add_pauli_string_linear_combinaison(self, other):
        """
        Adding with an other LCPS. Merging the coefs and PauliStrings arrays.

        Args:
            other (LinearCombinaisonPauliString): An other LCPS.

        Raises:
            ValueError: If other is not an LCPS.
            ValueError: If the other LCPS has not the same number of qubits.

        Returns:
            LinearCombinaisonPauliString: New LCPS of len = len(self) + len(other).
        """

        if not isinstance(other,LinearCombinaisonPauliString):
            raise ValueError('Can only add with an other LCPS')

        if self.n_qubits != other.n_qubits:
            raise ValueError('Can only add with LCPS of identical number of qubits')

        new_coefs = new_pauli_strings = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        # Hints : use np.concatenate
        new_coefs = np.concatenate((self.coefs, other.coefs))
        new_pauli_strings = np.concatenate((self.pauli_strings, other.pauli_strings))
        ################################################################################################################

        return self.__class__(new_coefs, new_pauli_strings)

    def mul_linear_combinaison_pauli_string(self, other):
        """
        Multiply with an other LCPS.

        Args:
            other (LinearCombinaisonPauliString): An other LCPS.

        Raises:
            ValueError: If other is not an LCPS.
            ValueError: If the other LCPS has not the same number of qubits.

        Returns:
            LinearCombinaisonPauliString: New LCPS of len = len(self) * len(other).
        """

        if not isinstance(other, LinearCombinaisonPauliString):
            raise ValueError()

        if self.n_qubits != other.n_qubits:
            raise ValueError('Can only add with LCPS of identical number of qubits')

        new_coefs = np.zeros((len(self)*len(other),), dtype=np.complex)
        new_pauli_strings = np.zeros((len(self)*len(other),), dtype=PauliString)
        
        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        
        for i in range(self.n_terms):
            for j in range(other.n_terms):
                new_pauli_strings[i * other.n_terms + j], phase = self.pauli_strings[i] * other.pauli_strings[j]
                new_coefs[i * other.n_terms + j] = self.coefs[i] * other.coefs[j] * phase

        return self.__class__(new_coefs, new_pauli_strings)

    def mul_coef(self,other):
        """
        Multiply the LCPS by a coef (numeric) or an array of the same length.

        Args:
            other (float, complex or np.array): One numeric factor or one factor per PauliString.

        Raises:
            ValueError: If other is np.array should be of the same length as the LCPS.

        Returns:
            [type]: [description]
        """

        new_coefs = new_pauli_strings = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        if isinstance(other, np.ndarray):
            if len(other) != self.__len__():
                raise ValueError("Array length does not equal length of LCPS!")
        new_coefs = self.coefs * other
        new_pauli_strings = self.pauli_strings
        ################################################################################################################

        return self.__class__(new_coefs, new_pauli_strings)

    def to_zx_bits(self):
        """
        Build an array that contains all the zx_bits for each PauliString.

        Returns:
            np.array<bool>: A 2d array of booleans where each line is the zx_bits of a PauliString.
        """

        zx_bits = np.zeros((len(self), 2*self.n_qubits), dtype=np.bool)

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        for i, ps in enumerate(self.pauli_strings):
            zx_bits[i, :] = ps.to_zx_bits()
        
        return zx_bits

    def to_xz_bits(self):
        """
        Build an array that contains all the xz_bits for each PauliString.

        Returns:
            np.array<bool>: A 2d array of booleans where each line is the xz_bits of a PauliString.
        """

        xz_bits = np.zeros((len(self), 2*self.n_qubits), dtype=np.bool)

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        for i, ps in enumerate(self.pauli_strings):
            xz_bits[i, :] = ps.to_xz_bits()

        return xz_bits

    def ids(self):
        """
        Build an array that identifies the position of all the I for each PauliString.

        Returns:
            np.array<bool>: A 2d array of booleans where each line is the xz_bits of a PauliString.
        """

        ids = np.zeros((len(self), self.n_qubits), dtype=np.bool)

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        ################################################################################################################
        
        for i, ps in enumerate(self.pauli_strings):
            ids[i, :] = ps.ids()

        return ids

    def combine(self):
        """
        Finds unique PauliStrings in the LCPS and combines the coefs of identical PauliStrings.
        Reduces the length of the LCPS.

        Returns:
            LinearCombinaisonPauliString: LCPS with combined coefficients.
        """

        new_coefs = new_pauli_strings = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        # hint : make use to_zx_bits and np.unique
        ################################################################################################################
        old_pauli_strings = self.to_zx_bits()
        new_pauli_strings_zx = np.unique(old_pauli_strings, axis=0)
        new_pauli_strings = np.array([PauliString.from_zx_bits(zx) for zx in new_pauli_strings_zx], dtype=PauliString)
        new_coefs = np.array([sum(self.coefs[(old_pauli_strings==u).all(axis=1)]) for u in new_pauli_strings_zx])

        return self.__class__(new_coefs, new_pauli_strings)

    def apply_threshold(self, threshold=1e-6):
        """
        Remove PauliStrings with coefficients smaller then threshold.

        Args:
            threshold (float, optional): PauliStrings with coef smaller than 'threshold' will be removed. 
                                         Defaults to 1e-6.

        Returns:
            LinearCombinaisonPauliString: LCPS without coefficients smaller then threshold.
        """

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        # Hint : create a np.array<bool> and use this array to get the subset of the lcps where this array is True
        ################################################################################################################
        
        new_lcps = self[np.abs(self.coefs) >= threshold]

        return new_lcps

    def divide_in_bitwise_commuting_cliques(self):
        """
        Find bitwise commuting cliques in the LCPS.

        Returns:
            list<LinearCombinaisonPauliString>: List of LCPS where all elements of one LCPS bitwise commute with each
                                                other.
        """

        cliques = list()

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.2)
        # This one can be hard to implement
        # Use to_zx_bits
        # Transform all I into Z and look for unique PauliStrings
        ################################################################################################################

        raise NotImplementedError()

        return cliques

    def sort(self):
        """
        Sort the PauliStrings using I<X<Y<Z and with LSB on the left.

        Returns:
            LinearCombinaisonPauliString: Sorted.
        """

        order = None

        ################################################################################################################
        # YOUR CODE HERE
        # TO COMPLETE (after activity 3.1)
        order = np.argsort([''.join((1*np.flip(bitstring)).astype(str)) for bitstring in self.to_zx_bits()])
        #order = np.argsort([str(ps) for ps in self.pauli_strings])
        ################################################################################################################

        new_coefs = self.coefs[order]
        new_pauli_strings = self.pauli_strings[order]

        return self.__class__(new_coefs, new_pauli_strings)
    
    def to_matrix(self):
        """
        Build the total matrix representation of the LCPS.

        Returns:
            np.array<complex>: A 2**n side square matrix.
        """

        size = 2**self.n_qubits
        matrix = np.zeros((size, size), dtype=np.complex)

        ################################################################################################################
        # YOUR CODE HERE (OPTIONAL)
        # TO COMPLETE (after activity 3.1)
        # Hints : sum all the matrices of all PauliStrings weighted by their coef
        ################################################################################################################

        matrix = sum([self.coefs[i]*self.pauli_strings[i].to_matrix() for i in range(self.n_terms)])

        return matrix


