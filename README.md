
# LEP


## Development environment
- Windows/Mac OS/Linux
- IDE: Pycharm Community [download](https://www.jetbrains.com/pycharm/download)

## Technology Keywords
- Git
- Python 3.6
- Flask web framework
- Docker
- Javascript
- Restful API
- Web charts

## How to run

#### Run in VM

    ```bash
    $ git clone https://github.com/linuxep/lepv.git
    $ export PYTHONPATH=$PYTHONPATH:$PWD/lepv
    $ cd lepv/app
    $ pip install -r requirements.txt
    $ python run.py
    ```

#### Run in Docker ( by building image locally )

    ```bash
    $ git clone https://github.com/linuxep/lepv.git
    $ ./buildImage.sh
    $ ./runContainer.sh
    ```

#### Run in Docker ( with one single command, without having to clone LEPV code )
    ```bash
    $ docker run -d -p 8889:8889 linuxep/lepv
    ```


## How to install Docker

#### From Docker official website
 - https://docs.docker.com/engine/installation/

#### From Aliyun which should be faster from inside Great Firewall
 - https://cr.console.aliyun.com/#/accelerator


## How to contribute
You can clone the repo by https://github.com/linuxep/lepv.git
But if you want to contribute ( which is encouraged and appreciated ), you should fork the repo.
 - You have no access to push to this repo, pull request is the way to get your code merged.
 - You can clone the repo and create your own repo, but without forking,
   the connection between your repo and this repo(its upstream) is lost, your pull request will not work

This is [How to fork a repo](https://help.github.com/articles/fork-a-repo/)
This is [Fork and pull request workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962)


