## Subnet Scanner for Unused IPs

Puprpose of this program is to find IPs that can be allocated to a server as static ones.

Program cheks IPs:
  - using ping
  - performing DNS lookup
  - checking if any of the below ports is listening:
      - 22
      - 3389
      - 80
      - 443

When run on clients (windows, macos) or UNIX as non-root user, pleas execute with **sudo**.
