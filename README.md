# bumpkin

[![codecov](https://codecov.io/gh/lucasew/bumpkin/branch/main/graph/badge.svg?token=bumpkin_token_here)](https://codecov.io/gh/lucasew/bumpkin)
[![CI](https://github.com/lucasew/bumpkin/actions/workflows/main.yml/badge.svg)](https://github.com/lucasew/bumpkin/actions/workflows/main.yml)

Tool to do source bumps :jack_o_lantern:

## Features
- Quick information fetch using the defined plugins
```shell
$ bumpkin demo basichttp https://discord.com/api/download?platform=osx
INFO:bumpkin.sources.basichttp:Downloading and hashing: https://dl.discordapp.net/apps/osx/0.0.273/Discord.dmg
{'sha256': '54794fbf4b29c9a56f6e8a736ff5445c75a1fd3cf49dce7b4d7aa6ff067ae2ef', 'final_url': 'https://dl.discordapp.net/apps/osx/0.0.273/Discord.dmg'}
```

- Evaluation with JSON files. See the examples folder.

```shell
$ cat examples/discord.json 
{
  "x86_64-linux": {
    "stable": {
        "_type": "basichttp",
        "url": "https://discord.com/api/download?platform=linux&format=tar.gz"
    },
    "ptb": {
        "_type": "basichttp",
        "url": "https://discord.com/api/download/ptb?platform=linux&format=tar.gz"
    },
    "canary": {
        "_type": "basichttp",
        "url": "https://discord.com/api/download/canary?platform=linux&format=tar.gz"
    }
  },
  "x86_64-darwin": {
    "stable": "https://discord.com/api/download?platform=osx",
    "ptb": "https://discord.com/api/download/ptb?platform=osx",
    "canary": "https://discord.com/api/download/canary?platform=osx"
  },
  "aarch64-darwin": {
    "ptb": "https://discord.com/api/download/ptb?platform=osx"
  }
}

$ bumpkin eval -i examples/discord.json -o /tmp/discord.json 

$ cat /tmp/discord.json  | jq
{
  "x86_64-linux": {
    "stable": {
      "sha256": "581726cbd7f018fab756cd7eee520e47b3a25bf7749193482a9e10e4d458042c",
      "final_url": "https://dl.discordapp.net/apps/linux/0.0.25/discord-0.0.25.tar.gz"
    },
    "ptb": {
      "sha256": "2e80e0de2c0ad7cac3b3353f75010ad3f27c0c8c6bab276c7df959a3c200464b",
      "final_url": "https://dl-ptb.discordapp.net/apps/linux/0.0.39/discord-ptb-0.0.39.tar.gz"
    },
    "canary": {
      "sha256": "d99ad20f23e3dc01eb882599fdb6f7d371f727ded34ee9fffd68e62273449b09",
      "final_url": "https://dl-canary.discordapp.net/apps/linux/0.0.148/discord-canary-0.0.148.tar.gz"
    }
  },
  "x86_64-darwin": {
    "stable": "https://discord.com/api/download?platform=osx",
    "ptb": "https://discord.com/api/download/ptb?platform=osx",
    "canary": "https://discord.com/api/download/canary?platform=osx"
  },
  "aarch64-darwin": {
    "ptb": "https://discord.com/api/download/ptb?platform=osx"
  }
}

```

## How it works
The basic primitive of bumpkin is a source, which is basically a reducer.

The reducer takes some parameters such as the URL, and exposes a `reduce` method. This method takes the previous state of the result data, or a empty dictionary, changes and then returns the new data. So, if the plugin has some handling to not refetch stuff if the URL or latest version didn't changed, for example, it has everything it needs at hand.

## Install it from PyPI (in the future)

```bash
pip install bumpkin
```

## Usage

```bash
$ python -m bumpkin
#or
$ bumpkin
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

