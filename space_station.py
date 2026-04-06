#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_station.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/06 11:12:29 by cehenrot        #+#    #+#               #
#  Updated: 2026/04/06 13:03:33 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from datetime import datetime
from typing import Optional

from Pydantic import BaseModel, Field, ValidatioError


class Spacestation(BaseModel):
    station_id: str = Field(..., min_lenght=3, max_len=10)
    name: str = Field(..., min_lenght=1, max_len=50)
    crew_size: str = Field(..., )


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")


if __name__ == "__main__":
    main()
