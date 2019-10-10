# -*- coding: utf-8 -*-

import json
from typing import Dict, Optional, Union

from elasticsearch import Elasticsearch
from robot.api import logger
from robot.utils import ConnectionCache


class ElasticsearchLibrary(object):
    """
    Library for working with Elasticsearch.

    Based on:
    | Python client for Elasticsearch | https://pypi.python.org/pypi/elasticsearch |

    == Dependencies ==
    | Python client for Elasticsearch | https://pypi.python.org/pypi/elasticsearch |
    | robot framework | http://robotframework.org |

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self) -> None:
        """ Initialization. """
        self._connection: Optional[Elasticsearch] = None
        self._cache = ConnectionCache()

    @property
    def connection(self) -> Elasticsearch:
        """Check and return connection to Elasticsearch.

        *Raises:*\n
            RuntimeError: if connection to Elasticsearch hasn't been created yet.

        *Returns:*\n
            Current connection to Elasticsearch.
        """
        if self._connection is None:
            raise RuntimeError('There is no open connection to Elasticsearch.')
        return self._connection

    def connect_to_elasticsearch(self, host: str, port: Union[int, str], alias: str = 'default') -> int:
        """
        Open connection to Elasticsearch.

        *Args:*\n
            _host_ - server host name;\n
            _port_ - port number;\n
            _alias_ - http-connection alias;\n

        *Returns:*\n
            Connection index.

        *Example:*\n
            | Connect To Elasticsearch | 192.168.1.108 | 9200 | alias=cluster1 |
        """
        port = int(port)
        try:
            self._connection = Elasticsearch([{'host': host, 'port': port}])
            self._connection.host = host
            self._connection.port = port
            return self._cache.register(self._connection, alias=alias)
        except Exception as e:
            raise Exception(f'Connect to Elasticsearch error: {e}')

    def disconnect_from_elasticsearch(self) -> None:
        """
        Close connection to Elasticsearch.

        *Example:*\n
            | Connect To Elasticsearch      | 192.168.1.108 | alias=cluster1 |
            | Disconnect From Elasticsearch |
        """
        self._connection = None

    def close_all_elasticsearch_connections(self) -> None:
        """
        Close all connections to ElasticSearch.

        This keyword is used to close all connections in case if there are several open connections.

        After execution of this keyword connection index returned by
        [#Connect To Elasticsearch|Connect To Elasticsearch] starts from 1.

        *Example:*\n
            | Connect To Elasticsearch            | 192.168.1.108 | alias=cluster1 |
            | Connect To Elasticsearch            | 192.168.1.208 | alias=cluster2 |
            | Close All Elasticsearch Connections |
        """
        self._connection = None
        self._cache.empty_cache()

    def switch_elasticsearch_connection(self, index_or_alias: Union[int, str]) -> int:
        """
        Switch between active connections with several clusters using their index or alias.

        Alias is set in keyword [#Connect To Elasticsearch|Connect To Elasticsearch]
        which also returns connection index.

        *Args:*\n
            _index_or_alias_ - connection index or alias;

        *Returns:*\n
            Previous connection index.

        *Example:* (switch by alias)\n
            | Connect To Elasticsearch        |  192.168.1.108 | 9200 | alias=cluster1 |
            | Connect To Elasticsearch        |  192.168.1.208 | 9200 | alias=cluster2 |
            | Switch Elasticsearch Connection |  cluster1      |

        *Example:* (switch by index)\n
            | ${cluster1}=                    | Connect To Elasticsearch        | 192.168.1.108 | 9200 |
            | ${cluster2}=                    | Connect To Elasticsearch        | 192.168.1.208 | 9200 |
            | ${previous_index}=              | Switch Elasticsearch Connection | ${cluster1}   |
            | Switch Elasticsearch Connection | ${previous_index}               |
            =>\n
            ${cluster1}= 1\n
            ${cluster2}= 2\n
            ${previous_index}= 2\n
        """
        old_index = self._cache.current_index
        self._connection = self._cache.switch(index_or_alias)
        return old_index

    def is_alive(self) -> bool:
        """
        Check availability of Elasticsearch.

        Sending GET-request of the following format: 'http://<host>:<port>/'

        *Returns:*\n
            bool True, if Elasticsearch is available.\n
            bool False in other cases.

        *Raises:*\n
            Exception if sending GET-request is impossible.

        *Example:*\n
            | ${live}= | Is Alive |
            =>\n
            True
        """

        try:
            info = self.connection.info()
            return info["cluster_name"] == "elasticsearch"
        except Exception as e:
            logger.debug(f"Exception {e} raised working with Elasticsearch on "
                         f"{self.connection.host} and {self.connection.port}")  # type: ignore
            raise

    def es_save_data(self, es_string: str) -> None:
        """
        Add data to Elasticsearch.

        *Args:*\n
            _es_string_ - string with data for Elasticsearch;\n

        *Example:*\n
            | Connect To Elasticsearch            | 192.168.1.108 | 9200 |
            | Es Save Data                        | some_string1  |
            | Close All Elasticsearch Connections |
        """
        json_str = json.dumps({"key": es_string})
        body = json.loads(json_str)
        self.connection.index(index='es', doc_type='es', id=1, body=body)

    def es_retrieve_data(self) -> Dict:
        """
        Get data from Elasticsearch.

        *Returns:*\n
            Data from Elastcisearch.

        *Example:*\n
            | Connect To Elasticsearch            | 192.168.1.108               | 9200 |
            | ${data}=                            | Wait Until Keyword Succeeds | 5x   | 10s | Es Retrieve Data |
            | Close All Elasticsearch Connections |
        """
        try:
            data = self.connection.get(index='es', doc_type='es', id=1)
            return data
        except Exception as e:
            logger.debug(f"Exception {e} raised working with Elasticsearch on "
                         f"{self.connection.host} and {self.connection.port}")  # type: ignore
            raise

    def es_search(self, es_string: str) -> Dict:
        """
        Search for data in Elasticsearch.

        *Args:*\n
            _es_string_ - string for searching in Elasticsearch;\n

        *Returns:*\n
            Search results from Elastcisearch.

        *Example:*\n
            | Connect To Elasticsearch            | 192.168.1.108 | 9200         |
            | ${search_result}=                   | Es Search     | some_string2 |
            | Close All Elasticsearch Connections |
        """
        try:
            search_result = self.connection.search(
                index="es",
                body={"query": {"match": {'key': es_string}}})
            return search_result
        except Exception as e:
            logger.debug(f"Exception {e} raised working with Elasticsearch on "
                         f"{self.connection.host} and {self.connection.port}")  # type: ignore
            raise
