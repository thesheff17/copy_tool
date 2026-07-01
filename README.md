# copy tool
As data storage requirements explode, I would like a better copy program.

# TLDR
```bash
mkdir ~/destdir/

# wget
wget https://raw.githubusercontent.com/thesheff17/copy_tool/refs/heads/main/copy_tool.py

# curl
curl -o copy_tool.py https://raw.githubusercontent.com/thesheff17/copy_tool/refs/heads/main/copy_tool.py

# run tool: provide source directory and destination directory
chmod +x ./copy_tool.py
./copy_tool src_directory ~/destdir
```

# why python
I feel python is one of the better langauges for reading, writing, and terminal output.  You should always understand the code you are running.  You should look at [copy_tool.py](https://github.com/thesheff17/copy_tool/blob/main/copy_tool.py) before you run anything in this repo.

# python 3rd party packages
I'm going to try to keep this script only using the standard library.  I don't want people dealing with pip installs or other things like virtualenvs to run a copy tool.  I want people to able to curl/wget this script and be using it.

# why did I write this tool? isn't there a bunch of copy tools out there?
Yes there are endless copy tools.  I wanted something I wrote myself and tested myself.  I also wanted it in a simple language like python so if it needed to be extended to other projects it can be.  I also wanted something as simple as possible to monitor elasped time and the copy.  All these copy tools out there (scp, rsync, cp, etc) have very limited support for total elasped time. I also generate `copy_tool.json` with the results.  Further analysis can we used to calc average of the copy speed over mutiple runs with this file.  I also wanted a script you are never prompted for further input.  If it can do the copy from A -> B it is going to do it.

# how do I use this over a network?
I use [samba](https://en.wikipedia.org/wiki/Samba_(software)) + CIFS to mount directories.  samba supports SMB multi channel setups.
```bash
sudo apt-get update && sudo apt-get install cifs-utils

# mount a read only endpoint
sudo mount \
  -t cifs \
  -o username=username,iocharset=utf8,vers=3.0,ro \
  //ip-address/share-name \
  /mnt/drive01
  ```

I have been testing a bunch of `smb.conf` settings.  This is what I change so far:
```
  # performance tuning
  # Enable SMB3 Multi-Channel
  server multi channel support = yes

   # Require SMB2 or higher (Multi-Channel only works with SMB2/3)
   server min protocol = SMB2
   # server max protocol = SMB3

   # Signing - required for Multi-Channel per the spec
   # Can be "auto", "mandatory", or "disabled"
   # "auto" allows negotiation - clients will use it
   server signing = auto

   # Bind Samba to specific interfaces
   # List the interfaces you want Samba to advertise and listen on
   interfaces = lo eth0 eth1
   # interfaces = lo eth0
   bind interfaces only = yes

   # Performance tuning
   socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=131072 SO_SNDBUF=131072
   read raw = yes
   write raw = yes
   max xmit = 65535
   dead time = 15

   use sendfile = yes
   aio read size = 1
   aio write size = 1
   ```
# what does the output look like:
```
./copy_tool.py /mnt/ssdlocal/ /home/ubuntu/copydest/
copy_tool.py started...
scanning source directory and calculating total size of files. please wait...
Found 6 files to copy (91,221.97 MB).

copying file: file1.txt        file size: 32,734 MB  | 0.0% estimated: 0.61 MB/s | copied: 2/6 (4 file(s) left) | waiting on 33% of files to be copied: --:--

timer link:
https://www.google.com/search?q=timer+for+6+minutes

copying file: file2.txt         file size: 0 MB  | 100.0% estimated: 668.59 MB/s | copied: 6/6 (0 file(s) left) | estimated total time remaining: 00M:00S

copy_tool.py completed. copied: 6 out of 6 files in 2 minute(s) 16 second(s) copy speed: 668.54 MB/s.
```

# how does this compare to `scp` 
I consistently get a little better speeds with the same data.  I'm not sure if it is the tuning with samba multi channel support or something else.  I'm going to keep testing.  Even if it is a little bit slower I like this script so much more.

```
copy_tool.py completed. copied: 6 out of 6 files in 2 minute(s) 16 second(s) copy speed: 668.54 MB/s.

scp was: 2m53.703s
```

# how can you tell if you are using samba multi channel support correctly? 
On the client I run.  Then I take a look at output.txt 

```
sudo cat /proc/fs/cifs/DebugData > output.txt

# output.txt sampe:

        Server interfaces: 4    Last updated: 603 seconds ago
        1)      Speed: 10Gbps
                Capabilities: rss
                IPv4: 192.168.1.11
                Weight (cur,total): (3,10)
                Allocated channels: 3
                [CONNECTED]

        2)      Speed: 10Gbps
                Capabilities: rss
                IPv4: 192.168.1.10
                Weight (cur,total): (1,10)
                Allocated channels: 1
                [CONNECTED]
```

- I also have set this variable based on recommendations. 
- Replace your interface name with the name below
```
sudo ethtool -L eth0 combined 6
```
# see an issue or need to discuss a feature/problem?
Please open a post in [discussions.](https://github.com/thesheff17/copy_tool/discussions) 

Open an [issues](https://github.com/thesheff17/copy_tool/issues) here.

Open a [PR](https://github.com/thesheff17/copy_tool/pulls) here.

