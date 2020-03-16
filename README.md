This repository is contains the notes, work, and code that I put together to complete the final project for CSE291-K00 at UCSD given during winter quarter 2020.

## Problem statement
The full problem statement is currently a living document and can be found on [Google Drive](https://docs.google.com/document/d/1nAF2tlBQOE3nhYV2yUQvsYLTYAmCpHDPv9vuqLhWXrU/edit?usp=sharing).
If you have trouble accessing it please contact me.

There were two motivations for this project.
The first is to practice implementing a mesh network.
I have been bitten by the decentralized network bug and I wanted to see how these kinds of networks are built from the ground up.
This is mostly a selfish goal, but I hope that in scratching my own itch I can help others learn a bit about OpenThread.
This leads to the second motivation:
to test the claims made by the Thread group, namely the self healing properties, low power consumption, and reliability of transmission.
I have designed four experiments to test these but I won't go into the details here.


## Structure of this repository
In the course of the project I tried quite a few things, but only a few of them *worked*.
This repository mostly has those things that did work, but I do note my major pitfalls so that anyone trying to recreate a similar project won't make the same mistakes I did.

This is **not** a clone of OpenThread; it is set of instructions and best practices that I have discovered while setting up my experiments.
Most of the *code* here is used for bootstrapping devices and performing network tests.
My notes are stored in markdown files so that you don't need to read through my code to work out why I did what I did.
