# lepv

**LEPV**, Linux Easy Profiling, is the front-end of LEP ( whose back-end is LEPD )

LEPV is a web-based application which visualizes the profiling of Linux based system, it's powerful yet intuitive to understand and easy to use.

We will release Docker image for LEPV soon, but before that happens, you can try build the image yourself, it's easy:

1. pull the latest lepv code, and go to its root directory

2. run this command to build the Docker image for LEPV:
   ./buildDockerImage.sh

3. run this command to run a Docker container for LEPV:
   ./runDockerContainer.sh

4. now visit "http://localhost:8889" from a web browser in your host machine.
