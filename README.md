Alga
====

A command line utility for controlling a LG webOS TV over the network.


Installing
----------

Alga is [available on PyPI](https://pypi.org/project/alga/).
I would recommend installing it via [pipx](https://pipx.pypa.io/stable/):

```shell
$ pipx install alga
```

Or, via [Nix flakes](https://nixos.org/):

```shell
nix run github:Tenzer/alga
```


Setup
-----

The first time you use the utility, you will need to setup a connection to the TV.
With the TV on, run `alga setup [hostname/IP]`.
This will bring up a prompt on the TV asking if you want to accept the pairing.
When accepted, Alga will be ready to use.

If no hostname or IP address is provided to `alga setup`, it will be default try to connect to "lgwebostv" which should work.

The hostname, a key and MAC address will be written to `~/.config/alga/config.json` for future use.

Note: It's currently only possible to pair Alga with one TV at a time.
Let me know if this is a deal breaker for you.


Usage
-----

See [usage](usage.md) for a list of available commands.


Development
-----------

The code base is fully type annotated and test coverage is being enforced.
Types can be checked via `poetry run mypy .` and tests via `poetry run pytest`.

Tests are run for each of the supported Python versions in CI.

[pre-commit](https://pre-commit.com/) used to run Ruff for linting and formatting.

`usage.md` is updated via `poetry run ./generate-usage.sh`.
