# mrit

Small toolbox for internet and networking tools written by
[myself](https://www.maxresing.de).

## ipinfo.py

Just a small script that reads a list of IP addresses from STDIN,
queries the data from [ipinfo.io](https://ipinfo.io) and writes the
response as a JSON response line by line to the STDOUT.

## massdig.py

Python-based wrapper around `dig` to bulk-lookup domain names. STDIN and
STDOUT are used as in- and output. A nameserver can be defined similar
to `dig` with the `@` operator, e.g. `@9.9.9.9`.

The tool ignores empty lines or lines that that start with '#', to allow
in-line comments.


## osinfo.sh

Shell tool to lookup OS information, e.g. the OS identifier and the
OS-like Linux distribution the OS is based on. Both features are
accessible through the commands `os` and `like`.


