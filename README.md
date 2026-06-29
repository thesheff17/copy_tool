# copy tool
As data storage requirements explode, we need a better copy file tool.  Really the answer is just start the copy and monitor the elasped total time and see if the time is acceptable.  If the total elapsed time is not acceptable, cancel the copy and re-evaluate.  

# why python
I feel python is one of the better langauges for reading, writing, and terminal output.  You should always understand the code you are running.  You should look at [copy_tool.py](https://github.com/thesheff17/copy_tool/blob/main/copy_tool.py) before you run anything in this repo.

# python 3rd party packages
My initial version used the `tqdm` package to calc and make a progress bar.  While I liked this I didn't like the idea of having a 3rd party dependency for people to use this script.  I want you to be able to wget/curl this file or just copy/paste and it works.  I have decided not include any 3rd party packages going forward.  This script really should work on any version of python3.12 and up.

# why did I write this tool? isn't there a bunch of copy tools out there?
Yes there are endless copy tools.  I wanted something I wrote myself and tested myself.  I also wanted it in a simple language like python so if it needed to be extended to other projects it can be.  I also wanted something as simple as possible to monitor elasped time.  All these copy tools out there (scp, rsync, cp, etc) have very limited support for total elasped time.

# how to use:
```bash
# create your DESTDIR
mkdir -p ~/DESTDIR

# wget
wget https://github.com/thesheff17/copy_tool/blob/main/copy_tool.py

# curl
curl -o copy_tool.py https://github.com/thesheff17/copy_tool/blob/main/copy_tool.py

# run script: pass directories without trailing slash
chmod +x ./copy_tool.py
./copy_tool.py /mnt/drive01 /home/ubuntu/copydest
```

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

# how is estimated min:sec remaining work?
At first I had this calc based on the number of bytes but this was all over the place.  I decided to just estimate this on the number of files copied over time vs files remaining to copy.  Note this is NOT 100% accurate.

# How is the google timer link calculated?
After 10% of the copy is complete the program will print out a timer link + 5 min.  This way you can easily go to this link and the timer will go off after x time.  I found most of the time + 5 min on these scripts the copy is usually completed.  Note this is NOT 100% accurate.  If you find out your timer is going off before the copy is done you can adjust the 5 min offset or/and try to adjust the 10% threshold variables.  The 5 min can easily be bumped to 10-15 min if needed.

# Why not try to display Mb/s during the transfer?
From my experience networks are all over the place on speed.  What really matters in the end is Mb/s over some time frame.  Lots of times I see dips to 120Mb/s but then the copy resumes faster speeds without the Mb/s counter being updated.  In the end I just care about total time and Mb/s over that time frame.

# what does the output look like:
```bash
./copy_tool.py /mnt/ssd01 /home/ubuntu/copydest
copy_tool.py started...
scanning source directory and calculating total size of files. please wait...
Found 76 files to copy (87,062.67 MB).

copying file: file1.txt  | 9.2% | copied: 8/76 (68 file(s) left) | estimated time remaining: 01M:04S

[10% completed] timer link:
https://www.google.com/search?q=timer+for+6+minutes

copying file: file2.txt  | 98.7% | copied: 76/76 (0 file(s) left) | estimated time remaining: 00M:00S

copy_tool.py completed. copied: 76 out of 76 files in 1 minute(s) 23 second(s) copy speed: 1039.84 MB/s.
```

# see an issue or need to discuss a feature/problem?
Please open a post in [discussions.](https://github.com/thesheff17/copy_tool/discussions) 

Open an [issues](https://github.com/thesheff17/copy_tool/issues) here.

Open a [PR](https://github.com/thesheff17/copy_tool/pulls) here.

