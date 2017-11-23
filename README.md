
# LEP


## Preferred development environment
- Windows/Mac OX/Linux, either works
- IDE: Pycharm Community

## Technology Keywords
- Git
- Python 3.6
- Flask web framework
- Docker
- Javascript
- Restful API
- Web charts

- Software Tools
    1. Python
    2. Docker
        install faster click [here](http://get.daocloud.io/)
    3. Flask  
        pip install Flask 
        `(pip install maybe  faster for append [ -i http://pypi.douban.com/simple ] or config /etc/pip.conf)`
- Start
    1. Run on VM
    ```bash
    $ git clone https://github.com/linuxep/lepv.git
    $ export PYTHONPATH=$PYTHONPATH:$PWD/lepv
    $ cd lepv/app
    $ pip install -r requirements.txt
    $ python run.py
    ```
    2. Build image
    ```bash
    $ ./buildImage.sh
    ```
    `For foreign networks or VPN:
    bash
    $ ./buildImage.sh us`
    3. Run in Docker
    ```bash
    $ ./runContainer.sh
    ```
    4. Open browser [127.0.0.1:8889](http://192.168.156.90:8889)

## Setup aliyun mirror and install docker
Access https://cr.console.aliyun.com/#/accelerator and follow steps there

## Verify docker installation
$ docker run hello-world
