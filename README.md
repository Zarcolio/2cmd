![](https://img.shields.io/github/license/Zarcolio/2cmd) ![](https://badges.pufler.dev/visits/Zarcolio/2cmd) ![](https://img.shields.io/github/stars/Zarcolio/2cmd) ![](https://img.shields.io/github/forks/Zarcolio/2cmd) ![](https://img.shields.io/github/issues/Zarcolio/2cmd) ![](https://img.shields.io/github/issues-closed-raw/Zarcolio/2cmd)  ![](https://img.shields.io/github/issues-pr/Zarcolio/2cmd) ![](https://img.shields.io/github/issues-pr-closed-raw/Zarcolio/2cmd)

# About 2cmd
How often do you come across a tool that does exactly what you want, but it does not take input from a file?
2cmd tries to fix this. It takes input from stdin and runs each line with the command(s) in the given config file providing you with the possibility to use input files with commands that don't support standard input or input files.

# Install
2cmd should be able to run with a default Kali Linux installation without installing additional Python packages. If you're running into trouble running 2cmd, please drop me an issue and I'll try to fix it :)

# Usage
```
2cmd [-h] [-hh] [-2 SECOND] [-t TIMEOUT] [-v] [-w WORKERS] cmd

This script takes input lines from stdin and inserts them in the commands
provided in the commands file. This way you can execute a certain command many
times. For example you can take screen shots of URLs with cutycapt provided by
output of another command.

positional arguments:
  cmd                   File containing one or more commands that should be
                        executed. If no path is provided, a file in
                        scriptdir/2cmd.xmpls is assumed. Use $2cmd$ or
                        $2cmdsan$ in lowercase in each command line. $2cmd$ is
                        replaced with each line from input. Use $cmdsan$ to
                        sanitize a string for use in a filename.

optional arguments:
  -h, --help            show this help message and exit
  -hh, --help2          Show the help inside the .2cmd script being called. Lines in the beginning of the script starting with # are displayed as help.
  -2 SECOND, --second SECOND
                        Pass a second variable to the script to run.
  -t TIMEOUT, --timeout TIMEOUT
                        Wait x milliseconds between commands.
  -v, --verbose         In green, show the commands that are created from 
                        stdin and the provide config file.
  -w WORKERS, --workers WORKERS
                        Defines how many worker threads execute the commands
                        in parallel.
```
# Examples
For example, [Wappalyzer cli](https://www.npmjs.com/package/wappalyzer-cli) has no support for providing an input file.
What if you have large sets of URLs to be analyzed with Wappalyzer?
You can do it manually, or create a script/oneliner.
But with 2cmd, it's possible run Wappalyzer with every URL that is provided through stdin.
A large number of example .2cmd files is located in the 2cmd.xmpls directory.

One for Wappalyzer is provided. It only contains:
```
wappalyzer $2cmd$ > $2cmdsan$.json
```
Want to analyze multiple URLs? Just create a file urls.txt:
```
https://www.google.com
https://www.uber.com
https://www.twitter.com
```
And run:
```
cat urls.txt | 2cmd wappalyzer.2cmd -v
```
This returns with standard output:
```
wappalyzer https://www.google.com > https-www.google.com.json
wappalyzer https://www.uber.com > https-www.uber.com.json
wappalyzer https://www.twitter.com > https-www.twitter.com.json
```
And 3 files containing the JSON output by Wappalyzer :)<br/>
Want one big file? Just edit the .2cmd file to to append to the output file:
```
wappalyzer $2cmd$ >> $2cmdsan$.json
```

Want to run nslookup against a list of FQDN's (A or SOA record)? Just run:
```
cat fqdns.txt | 2cmd nslookup_a.2cmd
```
Or:
```
cat fqdns.txt | 2cmd nslookup_soa.2cmd
```
If you want to show the help for a specific script (for example nslookup_a.2cmd), just run:
```
cat fqdns.txt | 2cmd nslookup_a.2cmd -hh
```
