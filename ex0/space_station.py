#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_station.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/06 11:12:29 by cehenrot        #+#    #+#               #
#  Updated: 2026/04/07 13:58:28 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
try:
    from datetime import datetime
    from typing import Optional
    from pydantic import BaseModel, Field, ValidationError
except ImportError as e:
    print(e)
    sys.exit(1)


class Spacestation(BaseModel):

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(None, min_length=0, max_length=200)


def main() -> None:

    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")

    try:
        model = Spacestation(
            station_id="SS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-04-06T16:30"),
            is_operational=True,
            notes="[Optimal]"
        )
    except ValidationError as e:
        print(f"Expected validation error: {e}")
        sys.exit(1)

    print(f"ID: {model.station_id}")
    print(f"Name: {model.name}")
    print(f"Crew: {model.crew_size}")
    print(f"Power: {model.power_level}")
    print(f"Oxygen: {model.oxygen_level}")
    print(f"Status: {model.last_maintenance}")
    print(f"Operational: {model.is_operational}")
    print(f"Notes: {model.notes}")

    print("\n========================================")
    print("Invalid station created:")

    try:
        model_2 = Spacestation(
            station_id="SS002",
            name="International Space Station",
            crew_size=26,
            power_level=50.5,
            oxygen_level=20.3,
            last_maintenance=datetime.fromisoformat("2026-04-06T16:30"),
            is_operational=False,
            notes="[Offeline]"
        )
    except ValidationError as e:
        print(f"Expected validation error: {e}")
        return

    print(f"ID: {model_2.station_id}")
    print(f"Name: {model_2.name}")
    print(f"Crew: {model_2.crew_size}")
    print(f"Power: {model_2.power_level}")
    print(f"Oxygen: {model_2.oxygen_level}")
    print(f"Status: {model_2.last_maintenance}")
    print(f"Operational: {model_2.is_operational}")
    print(f"Notes: {model_2.notes}")


if __name__ == "__main__":
    main()
