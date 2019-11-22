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

When run on clients (macos) or UNIX as non-root user, pleas execute with **sudo**.

By default program outputs to stdout in the form of the table. There is option to write optput to file as well.
This creates csv file in location defined in -o/--ouput switch.

Finally -q/--quiet switch supresses stdout and writes to log only.
