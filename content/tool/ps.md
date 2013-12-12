---
title: "ps"
date: 2013-08-17 07:32
---


report a snapshot of the current processes

If you want a repetitive update of the selection and the displayed information, use top instead.

ps accepts several kinds of options:

* UNIX options, which may be grouped and must be preceded by a dash.
* BSD options, which may be grouped and must not be used with a dash.
* GNU long options, which are preceded by two dashes.

Note:
`ps aux` vs `ps -aux`, the latter print all processes owned by user named 'x'

By default, ps selects all processes with the same effective user ID (euid=EUID) as the current user and associated with the same terminal as the invoker. It displays the process ID(pid=PID), the terminal associated with the process (tname=TTY), the cumulated CPU time in [DD-]hh:mm:ss format (time=TIME), and the executable name (ucmd=CMD). Output is unsorted by default.
