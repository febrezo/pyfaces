Pyfaces
=======

Copyright (C) 2020-2022  F. Brezo ([@febrezo](https://twitter.com/febrezo))

[![License](https://img.shields.io/badge/license-GNU%20Affero%20General%20Public%20License%20Version%203%20or%20Later-blue.svg)]()

1 - Description
---------------

Pyfaces is a Python3.6+ package which helps with working with face recognition tasks.

2 - License: GNU AGPLv3+
------------------------

This is free software, and you are welcome to redistribute it under certain conditions.

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


For more details on this issue, check the [COPYING](COPYING) file.

3 - Installation
----------------

This package makes use of `dlib` which has additional dependencies, depending on your OS. 
Taking this into account, proceed as you find easier, considering that the Docker approach needs additional knowledge of how volumes work and how they are mapped.

### Manual installation

One of the dependencies of the `dlib`framework is `cmake` which needs to be installed in your machine locally.

```
$ cmake --version
cmake version 3.10.2

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

If this throws an error, you will need to install it manually, using, for example:

- In Debian-based systems:

```
$ sudo apt install cmake
```

-  In Fedora-based systems:

```
$ sudo dnf install cmake
```

Once solved, the fast way to do it on any system for a user with administration privileges:

```
$ pip3 install pyfaces
```

Note that `dlib` installation may take some time. Really. You can upgrade to the latest release of the framework with:

```
$ pip3 install pyfaces --upgrade
```

This will manage the dependencies (mainly `face_recognition` and `dlib`) for you and install the latest version of the framework.

4 - Basic CLI Usage
-------------------

If everything went correctly (we hope so!), it's time for trying the CLI: `pyfaces`.

```
$ pyfaces --help

                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/



                     Coded with ♥ by Félix Brezo since 2020                    

                                 License: AGPLv3                                 


                       -- Stay safe and use your mask! --                       


usage: pyfaces [-h] [--version] <sub_command> <sub_command_options> ...

Pyfaces CLI | A face recognition tool to make it accesible for everyone and
learn from it to what extent we are exposed.

SUBCOMMANDS:
  List of available commands that can be invoked using Pyfaces CLI.

  <sub_command> <sub_command_options>
    compare             Compare two face files
    extract             Extract faces from a file and save encodings
    guess               Gues which is the most similar candidate to a knowon
                        face

About arguments:
  Showing additional information about this program.

  -h, --help            shows this help and exists.
  --version             shows the version of the program and exits.

```

### Using Docker

Note that if you use Docker you will not have to fix the dependencies yourself because they are already fixed in the container.
Check if you have Docker installed:

```
$ docker --version
Docker version 20.10.7, build 20.10.7-0ubuntu5~20.04.2
```

Then, simply clone the repository. 
If you have `git` installed, it is a simple as:

```
$ git clone https://github.com/febrezo/pyfaces 
$ cd pyfaces
```

Otherwise, download the latest `.zip` file and unzip it.

In any case, it's time to build the image in the folder:

```
$ docker build -t pyfaces
```

To run it, you have to consider that you WILL need to map the folders in which you have your images in your system onto the Docker container that you are creating.
For example, if your image folder in your own system was `/tmp` and you want to make it reachable within the container under `/images`, the running command to get a shell inside the container might look like this:

```
$ docker run -it -v /tmp:/images pyfaces bash
root@8aa2cab82c3e:/# pyfaces


                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/



                     Coded with ♥ by Félix Brezo since 2020                    

                                 License: AGPLv3                                 


             -- Yes: facial recognition is here, so take action! --             


usage: pyfaces [-h] [--version] <sub_command> <sub_command_options> ...

Pyfaces CLI | A face recognition tool to make it accesible for everyone and learn from it to what extent we are exposed.

SUBCOMMANDS:
  List of available commands that can be invoked using Pyfaces CLI.

  <sub_command> <sub_command_options>
    compare             Compare two face files
    extract             Extract faces from a file and save encodings
    guess               Gues which is the most similar candidate to a knowon face

About arguments:
  Showing additional information about this program.

  -h, --help            shows this help and exists.
  --version             shows the version of the program and exits.
```

5 - JSON-RPC Usage
------------------

For interacting with it using a different programming language, you might use `pyfacesd`.

### Manual Configuration

This will start a JSON RPC server that will let you perform the operations of the framework using the standard JSON RPC specification.

```
$ pyfacesd


                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/



                     Coded with ♥ by Félix Brezo since 2020                    

                                 License: AGPLv3                                 


                 -- Your face identifies you. Keep it safe! --                  


 * Running on http://localhost:12012/ (Press CTRL+C to quit)

```

To peform the different requests you can usage any JSON-RPC framework and language.
Even `curl` is an option.

```
$ curl -X POST \
 	-H 'Content-Type: application/json' \
 	-d '{"params": {}, "method": "info", "id": "1", "jsonrpc": "2.0"}' \
 	localhost:12012
{
  "result": {
    "name": "Pyfaces 0.1.0 JSON-RPC Server",
    "methods": [
      "compare",
      "config",
      "extract",
      "get_face",
      "get_image",
      "guess",
      "info",
      "set_config"
    ],
    "faces": 3
  },
  "id": "1",
  "jsonrpc": "2.0"
}
```

### Using Docker

The JSON-RPC server can also be started using Docker.
Assuming that you have not built the image as stated in the previous step, you can repeat the process:

```
$ docker --version
Docker version 20.10.7, build 20.10.7-0ubuntu5~20.04.2
```

Then, simply clone the repository. 
If you have `git` installed, it is a simple as:

```
$ git clone https://github.com/febrezo/pyfaces 
$ cd pyfaces
```

Otherwise, download the latest `.zip` file and unzip it.

In any case, it's time to build the image in the folder:

```
$ docker build -t pyfaces
```

To run it, you have to consider that you WILL need to map the folders in which you have your images in your system onto the Docker container that you are creating.
For example, if your image folder in your own system was `/tmp` and you want to make it reachable within the container under `/images` you will have to specify it manually.
At the same time, you will need to dedfine the ports that will be exposed outside the container to your host system.
The daemon started by `pyfacesd` starts the service by default in the container's port 12012. 
If you want to expose it outside the container you have to explicitly define it with `-p <desired_port_host>:12012`.
The running command to get a shell inside the container might look like this if the port to be used was the same:

```
$ docker run -it -v /tmp:/images -p 12012:12012 pyfaces


                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/



                     Coded with ♥ by Félix Brezo since 2020                    

                                 License: AGPLv3                                 


                       -- Stay safe and use your mask! --                       


[INFO] Pyfaces:  Starting JSON-RPC server using waitress…
[INFO] Pyfaces:  Serving on http://0.0.0.0:12012
```

It is relevant to say that the service in the container is expecting valid paths within the container.
That is to say, if volumes are not mapped with the same names in the host and the container, any kind of reference to the file MUST be provided considering that the service is running INSIDE the container.

### Using Docker-compose

The JSON-RPC server can also be started using Docker-compose, a tool that is really helpful to administer several services at once

```
$ docker-compose --version
docker-compose version 1.29.2, build unknown
```

Then, simply clone the repository. 
If you have `git` installed, it is a simple as:

```
$ git clone https://github.com/febrezo/pyfaces 
$ cd pyfaces
```

Otherwise, download the latest `.zip` file and unzip it.

In any case, it's time to build the image in the folder and start it:

```
$ docker-compose up --build


                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/



                     Coded with ♥ by Félix Brezo since 2020                    

                                 License: AGPLv3                                 


                       -- Stay safe and use your mask! --                       


[INFO] Pyfaces:  Starting JSON-RPC server using waitress…
[INFO] Pyfaces:  Serving on http://0.0.0.0:12012
```

The `--build` is only needed whenever you make changes in the code, so probably you might be using `docker-compose up` directly most of the times.

You also have to consider that you WILL need to map the folders in which you have your images in your system onto the Docker container that you are creating.
For example, if your image folder in your own system was `/tmp` and you want to make it reachable within the container under `/images` you will have to specify it manually in the `docker-compose.yml` file.

As said before, note again that the service in the container is expecting valid paths within the container.
That is to say, if volumes are not mapped with the same names in the host and the container, any kind of reference to the file MUST be provided considering that the service is running INSIDE the container.