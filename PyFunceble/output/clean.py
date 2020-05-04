"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the cleaning interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from os import sep as directory_separator
from os import walk

import PyFunceble


class Clean:
    """
    Provide the cleaning logic.

    .. note::
        By cleaning we mean the cleaning of the :code:`output` directory.

    :param list_to_test: The list of domains we are testing.
    :type list_to_test: list|None

    :param bool clean_all:
        Tell the subsystem if we need to clean all.
        Which include, of course, the output directory but also
        all other file(s) generated by our system.
    :param str file_path:
        The path to the file we tested.

        .. note::
            This is only relevant if you use the MariaDB/MySQL database.
    """

    def __init__(self, clean_all=False, file_path=None):
        # We clean the output directory.
        self.almost_everything(clean_all, file_path)

    @classmethod
    def file_to_delete(cls, all_files=False):
        """
        Return the list of file to delete.
        """

        # We initiate the directory we have to look for.
        directory = "{0}{1}".format(
            PyFunceble.OUTPUT_DIRECTORY, PyFunceble.OUTPUTS.parent_directory
        )

        if not directory.endswith(directory_separator):  # pragma: no cover
            # For safety, if it does not ends with the directory separator, we append it
            # to its end.
            directory += directory_separator

        # We initiate a variable which will save the list of file to delete.
        result = []

        for root, _, files in walk(directory):
            # We walk in the directory and get all files and sub-directories.

            for file in files:
                # If there is files in the current sub-directory, we loop
                # through the list of files.

                if file in [".gitignore", ".keep"]:
                    continue

                if (
                    not all_files and "logs" in root and ".log" in file
                ):  # pragma: no cover
                    continue

                # The file is not into our list of file we do not have to delete.

                if root.endswith(directory_separator):
                    # The root ends with the directory separator.

                    # We construct the path and append the full path to the result.
                    result.append(root + file)
                else:
                    # The root directory does not ends with the directory separator.

                    # We construct the path by appending the directory separator
                    # between the root and the filename and append the full path to
                    # the result.
                    result.append(root + directory_separator + file)  # pragma: no cover

        # We return our list of file to delete.
        return result

    @classmethod
    def databases_to_delete(cls):  # pragma: no cover
        """
        Set the databases files to delete.
        """

        # We initate the result variable.
        result = []

        if PyFunceble.CONFIGURATION.db_type == "json":
            # We initiate the directory we have to look for.
            directory = PyFunceble.CONFIG_DIRECTORY

            # We append the dir_structure file.
            result.append(
                "{0}{1}".format(
                    directory, PyFunceble.OUTPUTS.default_files.dir_structure
                )
            )

            # We append the iana file.
            result.append(
                "{0}{1}".format(directory, PyFunceble.OUTPUTS.default_files.iana)
            )

            # We append the public suffix file.
            result.append(
                "{0}{1}".format(
                    directory, PyFunceble.OUTPUTS.default_files.public_suffix
                )
            )

            # We append the inactive database file.
            result.append(
                "{0}{1}".format(directory, PyFunceble.OUTPUTS.default_files.inactive_db)
            )

            # We append the mining database file.
            result.append(
                "{0}{1}".format(directory, PyFunceble.OUTPUTS.default_files.mining)
            )

        return result

    def almost_everything(self, clean_all=False, file_path=False):
        """
        Delete almost all discovered files.

        :param bool clean_all:
            Tell the subsystem if we have to clean everything instesd
            of almost everything.
        """

        if (
            "do_not_clean" not in PyFunceble.INTERN
            or not PyFunceble.INTERN["do_not_clean"]
        ):
            # We get the list of file to delete.
            to_delete = self.file_to_delete(clean_all)

            if (
                not PyFunceble.abstracts.Version.is_local_cloned() and clean_all
            ):  # pragma: no cover
                to_delete.extend(self.databases_to_delete())

            for file in to_delete:
                # We loop through the list of file to delete.

                # And we delete the currently read file.
                PyFunceble.helpers.File(file).delete()

                PyFunceble.LOGGER.info(f"Deleted: {file}")

            if clean_all:  # pragma: no cover
                to_avoid = ["whois"]
            else:
                to_avoid = ["whois", "auto_continue", "inactive", "mining"]

            if not file_path:
                query = "DELETE FROM {0}"
            else:  # pragma: no cover
                query = "DELETE FROM {0} WHERE file_path = %(file_path)s"

            if PyFunceble.CONFIGURATION.db_type in [
                "mariadb",
                "mysql",
            ]:  # pragma: no cover

                with PyFunceble.engine.MySQL() as connection:
                    for database_name in [
                        y
                        for x, y in PyFunceble.engine.MySQL.tables.items()
                        if x not in to_avoid
                    ]:
                        lquery = query.format(database_name)

                        with connection.cursor() as cursor:
                            cursor.execute(lquery, {"file_path": file_path})

                            PyFunceble.LOGGER.info(
                                "Cleaned the data related to "
                                f"{repr(file_path)} from the {database_name} table."
                            )

            if (
                not PyFunceble.abstracts.Version.is_local_cloned() and clean_all
            ):  # pragma: no cover
                PyFunceble.load_config()

                PyFunceble.LOGGER.info(f"Reloaded configuration.")
