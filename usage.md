# Available commands

**Usage**:

```console
$ alga [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--tv TEXT`: Specify which TV the command should be sent to
* `--timeout INTEGER`: Number of seconds to wait before a response (default 10)
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `adhoc`: Send raw request to the TV
* `app`: Apps installed on the TV
* `channel`: TV channels
* `input`: HDMI and similar inputs
* `media`: Control the playing media
* `power`: Turn TV (or screen) on and off
* `remote`: Remote control button presses
* `sound-output`: Audio output device
* `tv`: Set up TVs to manage via Alga
* `version`: Print Alga version
* `volume`: Audio volume

## `alga adhoc`

Send raw request to the TV

**Usage**:

```console
$ alga adhoc [OPTIONS] PATH [DATA]
```

**Arguments**:

* `PATH`: [required]
* `[DATA]`

**Options**:

* `--help`: Show this message and exit.

## `alga app`

Apps installed on the TV

**Usage**:

```console
$ alga app [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `close`: Close the provided app
* `current`: Get the current app
* `info`: Show info about specific app
* `launch`: Launch an app
* `list`: List installed apps
* `pick`: Show picker for selecting an app.

### `alga app close`

Close the provided app

**Usage**:

```console
$ alga app close [OPTIONS] APP_ID
```

**Arguments**:

* `APP_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga app current`

Get the current app

**Usage**:

```console
$ alga app current [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga app info`

Show info about specific app

**Usage**:

```console
$ alga app info [OPTIONS] APP_ID
```

**Arguments**:

* `APP_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga app launch`

Launch an app

**Usage**:

```console
$ alga app launch [OPTIONS] APP_ID [DATA]
```

**Arguments**:

* `APP_ID`: [required]
* `[DATA]`

**Options**:

* `--help`: Show this message and exit.

### `alga app list`

List installed apps

**Usage**:

```console
$ alga app list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga app pick`

Show picker for selecting an app.

**Usage**:

```console
$ alga app pick [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alga channel`

TV channels

**Usage**:

```console
$ alga channel [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `current`: Get the current channel
* `down`: Change channel down
* `list`: List available channels
* `pick`: Show picker for selecting a channel.
* `set`: Change to specific channel
* `up`: Change channel up

### `alga channel current`

Get the current channel

**Usage**:

```console
$ alga channel current [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga channel down`

Change channel down

**Usage**:

```console
$ alga channel down [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga channel list`

List available channels

**Usage**:

```console
$ alga channel list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga channel pick`

Show picker for selecting a channel.

**Usage**:

```console
$ alga channel pick [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga channel set`

Change to specific channel

**Usage**:

```console
$ alga channel set [OPTIONS] VALUE
```

**Arguments**:

* `VALUE`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga channel up`

Change channel up

**Usage**:

```console
$ alga channel up [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alga input`

HDMI and similar inputs

**Usage**:

```console
$ alga input [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List available inputs
* `pick`: Show picker for selecting an input.
* `set`: Switch to given input

### `alga input list`

List available inputs

**Usage**:

```console
$ alga input list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga input pick`

Show picker for selecting an input.

**Usage**:

```console
$ alga input pick [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga input set`

Switch to given input

**Usage**:

```console
$ alga input set [OPTIONS] VALUE
```

**Arguments**:

* `VALUE`: [required]

**Options**:

* `--help`: Show this message and exit.

## `alga media`

Control the playing media

**Usage**:

```console
$ alga media [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `fast-forward`: Fast forward media
* `pause`: Pause media
* `play`: Play media
* `rewind`: Rewind media
* `stop`: Stop media

### `alga media fast-forward`

Fast forward media

**Usage**:

```console
$ alga media fast-forward [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga media pause`

Pause media

**Usage**:

```console
$ alga media pause [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga media play`

Play media

**Usage**:

```console
$ alga media play [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga media rewind`

Rewind media

**Usage**:

```console
$ alga media rewind [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga media stop`

Stop media

**Usage**:

```console
$ alga media stop [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alga power`

Turn TV (or screen) on and off

**Usage**:

```console
$ alga power [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `off`: Turn TV off
* `on`: Turn TV on via Wake-on-LAN
* `screen-off`: Turn TV screen off
* `screen-on`: Turn TV screen on
* `screen-state`: Show if TV screen is active or off

### `alga power off`

Turn TV off

**Usage**:

```console
$ alga power off [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga power on`

Turn TV on via Wake-on-LAN

**Usage**:

```console
$ alga power on [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga power screen-off`

Turn TV screen off

**Usage**:

```console
$ alga power screen-off [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga power screen-on`

Turn TV screen on

**Usage**:

```console
$ alga power screen-on [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga power screen-state`

Show if TV screen is active or off

**Usage**:

```console
$ alga power screen-state [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alga remote`

Remote control button presses

**Usage**:

```console
$ alga remote [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `send`: Send a button press to the TV

### `alga remote send`

Send a button press to the TV

**Usage**:

```console
$ alga remote send [OPTIONS] BUTTON
```

**Arguments**:

* `BUTTON`: [required]

**Options**:

* `--help`: Show this message and exit.

## `alga sound-output`

Audio output device

**Usage**:

```console
$ alga sound-output [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Show the current output device
* `pick`: Show picker for selecting a sound output...
* `set`: Change the output device

### `alga sound-output get`

Show the current output device

**Usage**:

```console
$ alga sound-output get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga sound-output pick`

Show picker for selecting a sound output device.

**Usage**:

```console
$ alga sound-output pick [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga sound-output set`

Change the output device

**Usage**:

```console
$ alga sound-output set [OPTIONS] VALUE
```

**Arguments**:

* `VALUE`: [required]

**Options**:

* `--help`: Show this message and exit.

## `alga tv`

Set up TVs to manage via Alga

**Usage**:

```console
$ alga tv [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Pair a new TV
* `list`: List current TVs
* `remove`: Remove a TV
* `rename`: Change the identifier for a TV
* `set-default`: Set the default TV

### `alga tv add`

Pair a new TV

**Usage**:

```console
$ alga tv add [OPTIONS] NAME [HOSTNAME]
```

**Arguments**:

* `NAME`: [required]
* `[HOSTNAME]`: [default: lgwebostv]

**Options**:

* `--help`: Show this message and exit.

### `alga tv list`

List current TVs

**Usage**:

```console
$ alga tv list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga tv remove`

Remove a TV

**Usage**:

```console
$ alga tv remove [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga tv rename`

Change the identifier for a TV

**Usage**:

```console
$ alga tv rename [OPTIONS] OLD_NAME NEW_NAME
```

**Arguments**:

* `OLD_NAME`: [required]
* `NEW_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga tv set-default`

Set the default TV

**Usage**:

```console
$ alga tv set-default [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `alga version`

Print Alga version

**Usage**:

```console
$ alga version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alga volume`

Audio volume

**Usage**:

```console
$ alga volume [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `down`: Turn volume down
* `get`: Get current volume
* `mute`: Mute audio
* `set`: Set volume to specific amount
* `unmute`: Unmute audio
* `up`: Turn volume up

### `alga volume down`

Turn volume down

**Usage**:

```console
$ alga volume down [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga volume get`

Get current volume

**Usage**:

```console
$ alga volume get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga volume mute`

Mute audio

**Usage**:

```console
$ alga volume mute [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga volume set`

Set volume to specific amount

**Usage**:

```console
$ alga volume set [OPTIONS] VALUE
```

**Arguments**:

* `VALUE`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alga volume unmute`

Unmute audio

**Usage**:

```console
$ alga volume unmute [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `alga volume up`

Turn volume up

**Usage**:

```console
$ alga volume up [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
