# check_dns
Monitoring of correspondence between domain names and IP address associated

Domain name is a name associated with a physical IP address on the Internet, easy to remember. The Domain name server (DNS) is a distributed database, for name resolution, which uses intensive replication and caching to achieve high scalability and resilience to failures. However, it was not designed for malicious attacks such as caching poisoning. Cache Poison attacks compromise the integrity of the server because they occur when false information is injected into the cache of a DNS server, affecting the accuracy of DNS lookups, leading to which traffic destined to an IP address is routed to another.

This Nagios plugin monitors domain names and corresponding IP address, both passed as arguments, alerting with critical state if incompatibilities are verified. By default, Google DNS is used, however, optionally the user can set the DNS server that suits it.

Mandatory arguments: The following arguments must be specified when the module is executed:
-H or – host used to specify the domain name.
-I or – hostaddress used to specify the associated IP address, or that is expected to be associated or name specified in the-h argument.

Optional arguments: The following arguments are optionally invoked, as user needs:
-V or – version used to query the module version.
-A or – author used to query the author's data.
-d or – dnsserver used to specify a DNS server where the query must be made, by default the Google DNS server (8.8.8.8) is used.

Command-Line Execution Example:
./check_dns.py -H https://github.com -I 198.224.42.133

