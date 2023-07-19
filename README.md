# PapersFromEverywhere

Thanks to Pybliometrics and Elsevier teams :)

## How to make this work

Short version: Take a look at this video (Spanish only) → [Cómo agilizar tu investigación científica para una tesis
](https://www.youtube.com/watch?v=zlSkiM5h7f4)

You will need an api key from the Elsevier Developer Portal first. Then you have to install these Python packages:

Run a terminal and put

```bash
$ pip install pybliometrics
$ pip install pandas
```

You have to paste the api key the first time you run the script. You can change it by modifiying the Pybliometrics config.ini file, too. 

If you need to work with proxies you have to install pysocks:

```bash
$ pip install pysocks
```

Proxy is optional for the Pybliometrics config.ini file. Here's an example:  

```
[Proxy]
ftp = http://xxx.xxx.xxx.xxx:80
http = socks5://xxx.xxx.xxx.xxx:80
https = http://xxx.xxx.xxx.xxx:80
```

Have fun!
