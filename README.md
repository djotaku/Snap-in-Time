Snap-in-Time
============

[![Lint and PyTest](https://github.com/djotaku/Snap-in-Time/actions/workflows/linttest.yml/badge.svg)](https://github.com/djotaku/Snap-in-Time/actions/workflows/linttest.yml)[![Documentation Status](https://readthedocs.org/projects/snap-in-time/badge/?version=latest)](https://snap-in-time.readthedocs.io/en/latest/?badge=latest)

script for btrfs backups to create hourly snapshots, remote backups, and cull the snapshots.

See the examples directory for some examples of scripts that could be used to run this program. Ideally, you'd be
running it hourly since snapshots don't take up a lot of space unless you have a large file that's constantly changing (like a large database).

Documentation: https://snap-in-time.readthedocs.io/en/latest/

As of [release v3.1.3])(https://github.com/djotaku/Snap-in-Time/releases/tag/v3.1.3) if you are running on a system with journald, you can type:

```bash
journalctl -t snapintime 

# this can get a little overwhelming so you limit by time

journalctl -t snapintime --since today

# or be more specific

journalctl -t snapintime --since "2026-09-19 08:00:00" --until "2026-09-21 10:00:00"

```
to get a structured log of the program's output. 

I have eliminated the file-based logging in favor of journald logging.

## Next up on the Roadmap

- figure out how to make this run via uvx so that it doesn't need to be installed in a dummy directory. (Make sure root can run uvx?) (issue #49)
- Fix the structured logging (issue #57) so that it's more useful for automating messages if something goes wrong.
- Update documentation once it can be launched via uvx. 

## AI Usage

From the project's creation in 2014 through to 2024 no AI was used in the development of this codebase.

- For [Release v3.0.0](https://github.com/djotaku/Snap-in-Time/releases/tag/v3.0.0) I used AI for the first time in this codebase to fix a long-standing bug in the culling algorithm that was not working correctly. 
- For [Release v3.1.3])(https://github.com/djotaku/Snap-in-Time/releases/tag/v3.1.3) to help me figure out why I was printing the same output to both logs.

## Dev Reminders

### UV


