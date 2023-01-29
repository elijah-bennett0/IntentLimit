# -*- coding: utf-8 -*-
"""
@Description		: IntentLimit Banner Operations
@Author			: Ginsu
@Date			: 6/22/22
@Version		: 2.0
"""

### Imports
import os
import random
###

__all__ = ["getBanner"]

### Code
def getBanner(ildir: str) -> str:
	file = open(os.path.join(ildir, "banners.txt"), 'r')
	banners = file.read().split("\t")
	banner = random.choice(banners)
	return banner
###

if __name__ == "__main__":
	pass
