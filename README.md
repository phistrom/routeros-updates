# RouterOS Update Check Tool

Check for and download RouterOS updates on the command line.

  - Download the latest update for the architecture you specify
  - Echo just the URL to the download
  - View patch notes

## Install
`$ pip install routeros-updates`

## Usage
### Download Package
Download the update package for the given architecture (mipsbe, arm, x86, etc.)

#### Template
`$ ros-updates download <arch>`

#### Examples
Download latest mipsbe main package from 'stable' channel

  `$ ros-updates download mipsbe`
  
Download latest optional packages zip for ARM from 'long term' channel and put in /tmp folder:

  `$ ros-updates --channel lts download arm --file /tmp`

Download latest ARM main package from 'stable' channel and match directory structure from the update site.
This creates a folder path like **./routeros/6.45.5/routeros-arm-6.45.5.npk**

  `$ ros-updates download arm --mirror`


### Echo URL
Echo the download URL instead of downloading it.

#### Template
`$ ros-updates url <arch>`

#### Examples
Echo the URL for the optional packages for the ARM architecture in the 'stable' channel:

`$ ros-updates url arm --package all`

Echo the URL for the main package for the x86 architecture in the 'testing' channel:

`$ ros-updates --channel testing url x86`

### Echo Patch Notes
Echo the patch notes for the given channel.

#### Template
`$ ros-updates notes`

#### Examples
Echo patch notes for the 'stable' channel.

`$ ros-updates notes`

Echo patch notes for the 'lts' channel

`$ ros-updates --channel lts notes`
