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

## icanhaz.py

This tool provides BGP information about a given IP. By default, the
script first looks up the public IP address of the local host. The
public IP is determined by calling {ipv4,ipv6}.icanhazip.com - which
dubbed this tool as well.

`-v --ip-version`

  Use this option to determine the IP version - by default IPv4. Must be
  in {4, 6}. Has only an effect when the IP is queried from
  `icanhazip.com`.

`-i --ip`

  Set an IP, if you not requesting the IP of the localhost. By default
  `127.0.0.1`.

`cmd`
  Define the BGP parameter your are looking for. Must be in {asn, cidr,
  ip, ptr}



## osinfo.sh

Shell tool to lookup OS information, e.g. the OS identifier and the
OS-like Linux distribution the OS is based on. Both features are
accessible through the commands `os` and `like`.


## wait4ip.py

Python script that blocks until the client has a new public IP. Useful
to test for VPN connections. The script blocks for at most 10 seconds,
before it returns a failure.

Sample usage:

```
wait_for_connection() {
    ip=$(curl -s https://ipv4.icanhazip.com)
    result=$(./wait4ip.py $ip)
    return $result
}

if wait_for_connection ; then
    echo "success"
else
    echo "failure"
fi
```

