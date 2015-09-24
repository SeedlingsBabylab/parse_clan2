# parse_clan2

This script parses .cha files and produces a csv file as output. This output will have this form:


tier  | word     | utterance_type | object_present | speaker | timestamp       | basic_level | comment
----- | ---------| -------------- | -------------- | ------- | --------------  | ----------- | -------
*MAN  | car+seat | d              | n              |  FAT    | 4989390_4990400 |             |  NA



## usage

```bash
$: python parse_clan2.py
```

This will open up a GUI window asking to select the .cha file you want to parse. Its output will be in the same folder as the file being parsed.


#### parse_clan2_check usage

This script checks to make sure the file was parsed completely, without leaving anything out. It takes the
frequency output from Clan as its first argument (clan command: freq +o3 +o clan_file.cha). The output from that command should be pasted into a .txt file.

```bash
$: python parse_clan2_check.py clan_freq_output.txt parse_clan2_output.csv
```


#### batch_parse_clan2 usage

There's also a helper script that runs parse_clan2 over a whole folder of .cha files. It's called
batch_parse_clan2.py.

```
$: python batch_parse_clan2.py /folder/with/cha/files  /output/folder
```

documentation on the wiki [here](http://wiki.bcs.rochester.edu/Seedlings/ClanA#For_.cha_files)
