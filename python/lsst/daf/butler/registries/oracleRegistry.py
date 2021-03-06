# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ("OracleRegistry", )

import re

from sqlalchemy import event
from sqlalchemy import create_engine


from lsst.daf.butler.core.config import Config
from lsst.daf.butler.core.registry import RegistryConfig

from .sqlRegistry import SqlRegistry, SqlRegistryConfig


class OracleRegistry(SqlRegistry):
    """Registry backed by a Oracle database.

    Parameters
    ----------
    config : `SqlRegistryConfig` or `str`
        Load configuration
    """

    @classmethod
    def setConfigRoot(cls, root, config, full):
        """Set any filesystem-dependent config options for this Registry to
        be appropriate for a new empty repository with the given root.

        Parameters
        ----------
        root : `str`
            Filesystem path to the root of the data repository.
        config : `Config`
            A Butler-level config object to update (but not a
            `ButlerConfig`, to avoid included expanded defaults).
        full : `ButlerConfig`
            A complete Butler config with all defaults expanded;
            repository-specific options that should not be obtained
            from defaults when Butler instances are constructed
            should be copied from `full` to `Config`.
        """
        super().setConfigRoot(root, config, full)
        Config.overrideParameters(RegistryConfig, config, full,
                                  toCopy=("cls", "deferDatasetIdQueries"))

    def __init__(self, registryConfig, schemaConfig, dimensionConfig, create=False,
                 butlerRoot=None):
        registryConfig = SqlRegistryConfig(registryConfig)
        self.schemaConfig = schemaConfig
        super().__init__(registryConfig, schemaConfig, dimensionConfig, create,
                         butlerRoot=butlerRoot)

    def _createEngine(self):
        tables = self.schemaConfig['tables'].keys()

        # The following two function are used to ensure all table names are
        # properly quoted when executing sql statements. These are needed
        # because at present the Oracle database does not handle the case
        # sensitivity of the Table names correctly without being quoted.
        # This code may be able to be dropped in the future at such a time
        # as the database is changed for different case sensitivity
        # behavior
        def _ignoreQuote(name, matchObj):
            """ This function conditionally adds quotes around a given name
            in a block of text if it has not already been quoted by either
            single or double quotes
            """
            text = matchObj.group(0)
            if text.startswith("'") and text.endswith("'"):
                return text
            elif text.startswith('"') and text.endswith('"'):
                return text
            else:
                return text.replace(name, f'"{name}"')

        def _oracleExecute(connection, cursor, statement, parameters, context, executemany):
            """ This function compares the text of a sql query against a known
            list of table names. If any name is found in the statement, the
            name is replaced with a quoted version of that name if it is
            not already quoted.
            """
            for name in tables:
                if name in statement:
                    # Regex translated: Optional open double quote, optional
                    # single quote table name, word boundary, optional close
                    # single quote, optional close double quote
                    statement = re.sub(f"\"?'?{name}\\b'?\"?", lambda x: _ignoreQuote(name, x), statement)
            return statement, parameters
        engine = create_engine(self.config["db"], pool_size=1)
        event.listen(engine, "before_cursor_execute", _oracleExecute, retval=True)
        return engine
