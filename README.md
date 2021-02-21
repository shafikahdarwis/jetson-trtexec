# Trtexec Execution



## Step To Run the TRTEXEC
1. **Initialization**

## Initialize trtexec
```
$ cd /usr/src/tensorrt/bin/
$ echo -e "\n# trtexec" >> ~/.bashrc
$ echo export trtexec=`pwd`/trtexec >> ~/.bashrc
$ source ~/.bashrc
```

### Initialize models

#### tensorrt models
```
$ cd /usr/src/tensorrt/data/
$ echo -e "\n# data" >> ~/.bashrc
$ echo export data=`pwd` >> ~/.bashrc
$ source ~/.bashrc
```

#### jetson-inference
```
$ cd jetson-inference/data/networks
$ echo -e "\n# data1" >> ~/.bashrc
$ echo export data=`pwd` >> ~/.bashrc
$ source ~/.bashrc
```

#### jetson_benchmarks
```
$ cd jetson_benchmarks/models
$ echo -e "\n# data2" >> ~/.bashrc
$ echo export data=`pwd` >> ~/.bashrc
$ source ~/.bashrc
```


