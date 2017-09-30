
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

## How to set up development environment

- Software Tools
    1. Python
    2. Docker
        install faster click [here](http://get.daocloud.io/)
    3. Flask  
        pip install Flask `(pip install maybe  faster for append [ ** -i http://pypi.douban.com/simple** ] or config /etc/pip.conf)`
- Start
    1. Run on VM
    ```bash
    $ git clone https://github.com/linuxep/lepv.git
    $ export PYTHONPATH=$PYTHONPATH:$PWD/lepv
    $ cd lepv/app
    $ pip install -r requirements.txt
    $ python run.py
    ```
    2. Run in Docker
    ```bash
    $ ./buildImage.sh
    $ ./runContainer.sh
    ```
    3. Open browser [http:127.0.0.1:8889](http:127.0.0.1:8889)

## How to run in docker
1. TODO


