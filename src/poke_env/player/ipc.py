# -*- coding: utf-8 -*-
"""This module abstract the inter process communication (IPC) protocol.

Two protocols are supported:
 - websockets: reliable message-oriented channel over TCP, as used by showdown.
 - unix sockets: reliable stream-oriented channel for local IPC on Unix systems.
"""

from __future__ import annotations
from abc import abstractmethod, ABC
from asyncio import StreamReader, StreamWriter, open_unix_connection
import websockets


class EOFException(Exception):
    """Exception thrown when reaching EOF in a channel"""

    pass


class AbstractChannel(ABC):
    """A class containing a subset of methods exposed by the websockets API"""

    @abstractmethod
    async def send(self, message: str):
        pass

    @abstractmethod
    async def recv(self) -> str:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aiter__(self):
        """Iterate on received messages"""
        try:
            while True:
                yield await self.recv()
        except EOFException:
            return


class UnixChannel(AbstractChannel):
    """A channel based on Unix socket in stream mode (`SOCK_STREAM`)."""

    def __init__(self, path: str):
        super().__init__()
        self._writer: StreamWriter
        self._reader: StreamReader
        self._path = path
        self._separator = b"|"

    async def send(self, message: str):
        print(f"Sending: {message}")
        self._writer.writer(message)
        await self._writer.drain()

    async def recv(self) -> str:
        message = await self._reader.readuntil(self._separator)
        message = message.decode("utf-8")
        if len(message) == 0 and self._reader.at_eof():
            raise EOFException()
        print(f"Received: {message}")
        return message

    async def __aenter__(self) -> UnixChannel:
        (reader, writer) = await open_unix_connection(self._path)
        self._writer = writer
        self._reader = reader
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._writer.close()
        await self._writer.wait_closed()


def connect(server_url: str, is_unix: bool) -> AbstractChannel:
    """Create an IPC channel, either Unix or Websocket."""
    if is_unix:
        return UnixChannel(server_url)
    return websockets.connect(server_url, max_queue=None)
