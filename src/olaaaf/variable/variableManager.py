"""
Class used to store all non-anonymous user-declared `olaaaf.variable.variable.Variable`
and allow easy retrieving of already defined ones.
"""

from __future__ import annotations

from .variable import Variable

import re

class VariableManager:
    """
    VariableManager class, used to manage all instances of `olaaaf.variable.variable.Variable`.
    
    Attributes
    ----------
    instance: dictionary of Variable by String
        A dictionary of all instances of `olaaaf.variable.variable.Variable`, with their name as key.

    """
    
    instance = {}
    __namePatern = "^[a-zA-Z]([a-zA-Z0-9:_])*$"

    @staticmethod
    def verify(name: str, cls: type[Variable]) -> None:
        """
        Function verifying if a `olaaaf.variable.variable.Variable` can be added to `olaaaf.variable.variableManager.VariableManager.instance`,
        meaning that the name respects the naming conventions and that it doesn't already exists under another type.
    
        Parameters
        ----------
        name: String
            Name of the `olaaaf.variable.variable.Variable`.

        cl: class
            Type of the `olaaaf.variable.variable.Variable`.
        
        Raises
        ------
        TypeError
            If the object is already defined with another type or its name is not valid.
        """
        # We verifie constraint linked to the name of the variable
        if not re.match(VariableManager.__namePatern, name):
            raise NameError(f"{name} is not a valid name for a variable")
        # And then we test the classe of the variable
        if name in __class__.instance and cls !=  __class__.instance[name].__class__:
            raise TypeError(f"{name} is already define with another type.")

    @staticmethod
    def add(obj: Variable) -> Variable:
        """
        Function adding a `olaaaf.variable.variable.Variable` to `olaaaf.variable.variableManager.VariableManager.instance`.
    
        Parameters
        ----------
        obj: olaaaf.variable.variable.Variable
            The `olaaaf.variable.variable.Variable` to add.
        
            
        Returns
        -------
        olaaaf.variable.variable.Variable
            The `olaaaf.variable.variable.Variable` added if the execution of this function was successful.

        Raises
        ------
        TypeError
            If the object isn't a `olaaaf.variable.variable.Variable`, already defined with another type or its name is not valid.

        """

        VariableManager.verify(obj.name, obj.__class__)
        if(isinstance(obj, Variable)):
            __class__.instance[obj.name] = obj
            return obj
        else:
            raise TypeError(f"{obj} is not a Variable.")
    
    @classmethod
    def get(cls, name : str) -> Variable:
        """
        Function to get a `olaaaf.variable.variable.Variable` from the `olaaaf.variable.variableManager.VariableManager.instance`.
    
        Parameters
        ----------
        name: String
            The name of the `olaaaf.variable.variable.Variable` to get.
        
        Returns
        -------
        olaaaf.variable.variable.Variable
            The `olaaaf.variable.variable.Variable` to get.

        Raises
        ------
        NameError
            The Variable isn't defined.
        """
        
        if(name in cls.instance):
            return cls.instance[name]
        else: raise NameError(f"{name} is not declared.")
    
    @staticmethod
    def declare(name: str, cls: type[Variable]) -> Variable:
        """
        Function to declare a `olaaaf.variable.variable.Variable`.
    
        Parameters
        ----------
        name: String
            Name of the `olaaaf.variable.variable.Variable`.

        cl: class
            Type of the `olaaaf.variable.variable.Variable`.

        Returns:
        Variable
            The newly defined `olaaaf.variable.variable.Variable`.
        """
        
        obj = cls.__new__(name)
        return obj