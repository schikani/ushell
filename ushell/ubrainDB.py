# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

# This scripts is from brainDB project with minor modifications to integrate it with ushell.
# brainDB project is hosted at https://github.com/schikani/brainDB

import uos
import uerrno
import btree


class ubrainDB:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self._verbose = 0
        self._notClosed = True
        self._db = None

        # Try to make the database folder if it doesn't exist.
        try:
            uos.mkdir(self.path)

        except OSError as exc:
            if exc.args[0] == uerrno.EEXIST:
                pass

        self._initialize()

    # This function will try to open the database and save it's name.
    def _initialize(self):
        try:
            self._stream = open("/".join((self.path, self.name)), "r+b")
        except OSError:
            self._stream = open("/".join((self.path, self.name)), "w+b")

        self._db = btree.open(self._stream)

    # This function helps in displaying the message when database is closed.
    def _close_message(self):
        return "Database => '{}' is closed. Use reopen() to open the database again".format(self.name)

    # This function helps in re-opening the database after it is closed.
    def reopen(self):
        self._notClosed = True
        return self._initialize()

    # Verbose can be set to 1 for displaying writing / deleting messages.
    def verbose(self, value):
        if self._notClosed:
            if value >= 1:
                self._verbose = 1

            else:
                self._verbose = 0
        else:
            return self._close_message()

    # This function takes the key and value to be written in the current database.
    def write(self, key, value):
        if self._notClosed:

            try:
                display = ""
                if self._db is not None:
                    if self._verbose == 1:
                        display = "Writing to => '{0}' | Key => {1} |" \
                                  " Value => {2}" \
                            .format(self.name, type(key), type(value))

                    self._db[str(key).encode()] = str(value).encode()
                    self._db.flush()

                    return display

            except OSError:
                self._db.flush()
                return "Something went wrong while writing to => '{}' ".format(self.name)
        else:
            return self._close_message()

    # This function returns the data given it's key or value from the current database.
    # If a key is given as parameter, it returns value and if value is given as parameter,
    # a list of keys is returned
    def read(self, key=None, value=None):
        if self._notClosed:
            try:
                if key is not None:
                    try:
                        value_B = self._db[str(key).encode()]

                        try:
                            value_ = eval(value_B)

                        except NameError:
                            # Check if the data is type str
                            # decode() will decode from bytes to str
                            value_ = value_B.decode()

                        except SyntaxError:
                            # Check for any special characters
                            value_ = value_B.decode()

                        return value_

                    except KeyError:
                        raise KeyError

                elif value is not None:

                    keys = []

                    for key_, value_ in self._db.items():
                        if value_ == str(value).encode():
                            try:
                                keys.append(eval(key_))

                            except NameError:
                                keys.append(key_.decode())

                            except SyntaxError:
                                keys.append(key_.decode())

                    if len(keys) == 0:
                        raise KeyError

                    else:
                        return keys

            except OSError:
                return "Can't read from Database => '{}' ".format(self.name)

        else:
            return self._close_message()

    # Remove key-value pair/s given the key or value as the parameter.
    def remove(self, key=None, value=None):
        if self._notClosed:
            display = ""
            if key is not None:
                try:
                    if self._verbose == 1:
                        display = "Removing Key => {} ".format(type(key))
                    del self._db[str(key).encode()]
                    self._db.flush()

                    return display

                except KeyError:
                    raise KeyError

            elif value is not None:

                key_found = 0

                for key_, value_ in self._db.items():
                    if value_ == str(value).encode():
                        key_found = 1

                        if self._verbose == 1:
                            try:
                                k = eval(key_)
                            except NameError:
                                k = key_.decode()
                            except SyntaxError:
                                k = key_.decode()
                            display = "Removing Key => {} | By Value => {} ".format(type(k), type(value))

                        del self._db[key_]
                        self._db.flush()

                if key_found == 0:
                    raise KeyError
                else:
                    return display

            else:
                return "Enter a key or value to remove key-value pair/s"

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted keys in a list.
    # If key is given as start_key parameter, the keys after the key (including the given key)
    # to the end of database is returned as a sorted list.
    # If reverse is set True, the list is returned in reverse order.
    def keys(self, start_key=None, reverse=False):

        if self._notClosed:

            keys = []

            if start_key is not None:
                for k in self._db.keys(str(start_key).encode()):
                    try:
                        keys.append(eval(k))
                    except NameError:
                        keys.append(k.decode())
                    except SyntaxError:
                        keys.append(k.decode())
            else:
                for k in self._db.keys():
                    try:
                        keys.append(eval(k))
                    except NameError:
                        keys.append(k.decode())
                    except SyntaxError:
                        keys.append(k.decode())

            if reverse:
                keys.reverse()

            return keys

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted values in a list.
    # If key is given as start_key parameter, the values after the value (including the value of given key)
    # to the end of database is returned as a sorted list.
    # if reverse is set True, the list is returned in reverse order.
    def values(self, start_key=None, reverse=False):

        if self._notClosed:

            values = []

            if start_key is not None:
                for v in self._db.values(str(start_key).encode()):
                    try:
                        values.append(eval(v))
                    except NameError:
                        values.append(v.decode())
                    except SyntaxError:
                        values.append(v.decode())

            else:
                for v in self._db.values():
                    try:
                        values.append(eval(v))
                    except NameError:
                        values.append(v.decode())
                    except SyntaxError:
                        values.append(v.decode())

            if reverse:
                values.reverse()

            return values

        else:
            return self._close_message()

    # Get all encoded key - value pairs in a dictionary.
    # Optionally start_key param accepts a key.
    # The keys and values are stored as bytes objects.
    def items(self, start_key=None):

        if self._notClosed:

            items = {}

            if start_key is not None:
                for k, v in self._db.items(str(start_key).encode()):
                    items[k] = v
            else:
                for k, v in self._db.items():
                    items[k] = v

            return items

        else:
            return self._close_message()

    # Get a list of all the databases
    def databases(self):

        databases = [i[0] for i in uos.ilistdir(self.path)]

        return databases

    # Remove a database by it's name.
    def remove_database(self, name):

        try:
            display = "Removing Database => '{}' ".format(name)
            uos.remove("/".join((self.path, name)))

            if self._verbose == 1:
                return display

        except OSError:
            return "Database => '{}' not found".format(name)

    # This function helps in closing the current stream.
    # After calling this function, reading / writing  will not work.
    # In order to read / write again to the current instance, call reopen().
    def close(self):
        self._notClosed = False
        self._db.close()
        self._stream.close()
        if self._verbose == 1:
            return self._close_message()
