# -*- coding: utf-8 -*-
"""This module contains objects related to server configuration.
"""
from collections import namedtuple


ServerConfiguration = namedtuple(
    "ServerConfiguration", ["server_url", "authentication_url", "is_unix"]
)
"""Server configuration object. Represented with a tuple with two entries: server url
and authentication endpoint url."""

UnixServerConfiguration = ServerConfiguration(
    "/tmp/poke-env-ipc.sock",
    "https://play.pokemonshowdown.com/action.php?",
    True,
)
"""Server configuration with local Unix server and smogon's authentication endpoint."""

LocalhostServerConfiguration = ServerConfiguration(
    "localhost:8000",
    "https://play.pokemonshowdown.com/action.php?",
    False,
)
"""Server configuration with localhost and smogon's authentication endpoint."""

ShowdownServerConfiguration = ServerConfiguration(
    "sim.smogon.com:8000",
    "https://play.pokemonshowdown.com/action.php?",
    False,
)
"""Server configuration with smogon's server and authentication endpoint."""
