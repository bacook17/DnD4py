# DnD4py - A collection of codes for D&D 5th Edition

## Installation
`DnD4py` can be installed through [pip](https://pip.pypa.io/en/stable) via

```
pip install DnD4py
```

It can also be installeded by running
```
make install
```
from inside the respository.

## Usage

DnD4py contains a number of miscelanious codes for use with D&D 5th edition. They include:

### Roll4Me

Simulate a complex roll of many dice and modifiers
Gives result, individual rolls, the mean of the distribution and the percentile of that roll relative to the distribution.

Example:
```bash
$ roll 3d8 + 1d6 + 10
```
returns a roll similar to:
```
*************
Total:   25
*************
= 12      + 3   + 10
[7 2 3] + [3] + 10
Mean: 27.0
Percentile: 28.9%
```

### Lookup5e

Lookup D&D terms on Roll20. 

Currently supported: spells, items, and monsters

Example:
```bash
$ lookup5e potion of healing
```
returns
```
Potion Of Healing

Item Type: Adventuring Gear
Subtype: Potion
Weight: 0.5

Description
===========================
You regain 2d4 + 2 hit points when you drink this potion.  The potion's red
liquid glimmers when agitated.
```

You can shorten the lookup time if you know what category your search falls under:

```bash
$ lookup5e --monster goblin
```
is also identical to
```bash
$ monster5e goblin
```
with both returning:
```
Goblin

HP: 7 (2d6)
AC: 15 (Leather Armor, Shield)
Speed: 30 ft.
Challenge Rating: 1/4

STR	DEX	CON	INT	WIS	CHA
8 (-1)	14 (+2)	10 (+0)	10 (+0)	8 (-1)	8 (-1)

Type: humanoid (goblinoid)
Size: Small
Alignment: Neutral Evil
Senses: Darkvision 60 Ft.
Skills: Stealth +6
Languages: Common, Goblin


Description
===========================
*Traits*
Nimble Escape: The goblin can take the Disengage or Hide action as a
bonus action on each of its turns.

*Actions*
Scimitar: Melee Weapon Attack: +4
to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage.

Shortbow:
Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2)
piercing damage.
```

You can also try:
```
$ spell5e fireball
```
and
```
$ item5e deck of many things
```
