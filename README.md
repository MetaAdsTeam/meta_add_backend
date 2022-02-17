# Meta_Add

An interoperable software that aggregates the Metaverse and Real World Ad Space 
with A NEAR Smart contract acts as an agreement between parties.

## Getting Started

Before we start, I would like to note that this software product is just a 
backend. For full-fledged work, it will be necessary to install a [frontend](https://github.com/MetaAdsTeam) and 
figure out how [Decentraland](https://decentraland.org/) and [Addreality](https://addreality.com/) work. I also recommend getting 
acquainted with the work of the NEAR cryptocurrency and the [MetaMask](https://metamask.io/) crypto wallet & gateway to blockchain apps. 
Application use web3 token. Authorization takes place on a bundle of the frontend and the [MetaMask plugin](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn).

## Installation

    git clone <this repo>

    pip3 install -r requirements.txt
    cp ./meta_add/default.yaml ./meta_add/config.yaml

Edit `./meta_add/config.yaml` with your DB and server requirements using examples. 

    python3 ./meta_add/scripts/utils/db_init.py
    
## Run app
    
    python3 ./meta_add/scripts/run_api.py
