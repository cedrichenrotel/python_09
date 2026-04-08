# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_crew.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/07 14:14:01 by cehenrot        #+#    #+#               #
#  Updated: 2026/04/08 08:32:32 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
try:
    from datetime import datetime
    from typing import List
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from enum import Enum
except ImportError as e:
    print(e)
    sys.exit(1)


class RankEnum(Enum):
    cadet = 'cadet'
    officer = 'officer'
    lieutenant = 'lieutenant'
    captain = 'captain'
    commander = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: RankEnum
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1, le=10000.0)

    @model_validator(mode='after')
    def MissionValidation(self) -> 'SpaceMission':
        half = len(self.crew) // 2
        insuf_xp = len([i for i in self.crew if i.years_experience < 5])

        if not self.mission_id.startswith('M'):
            raise ValueError("[WARNING] -> The mission ID does not begin "
                             "with 'M'")
        elif not any(m.rank == RankEnum.captain or
                     m.rank == RankEnum.commander for m in self.crew):
            raise ValueError("[WARNING] -> A missing commander or captain")
        elif self.duration_days > 365 and half < insuf_xp:
            raise ValueError("[WARNING] -> More than 50% of crews do not "
                             "have the required number of years service "
                             "(5+ years)")
        elif not any(m.is_active is True for m in self.crew):
            raise ValueError("[WARNING] -> inactive crew members")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    try:
        print("Valid mission created:")
        test1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500.0,
            launch_date=datetime.fromisoformat("2026-03-07T19:38"),
            crew=[
                CrewMember(
                    member_id="SC001",
                    name="Sarah Connor",
                    rank=RankEnum.commander,
                    age=35,
                    specialization="Mission Command",
                    years_experience=10,
                    is_active=True
                ),
                CrewMember(
                    member_id="SC002",
                    name="John Smith",
                    rank=RankEnum.lieutenant,
                    age=20,
                    specialization="Navigation",
                    years_experience=10,
                    is_active=True
                ),
                CrewMember(
                    member_id="SC003",
                    name="Alice Johnson",
                    rank=RankEnum.officer,
                    age=18,
                    specialization="Engineering",
                    years_experience=5,
                    is_active=True
                )
            ]
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"Field: {error['loc']} - Error: {error['msg']}")
        sys.exit(1)

    print(f"ID: {test1.mission_id}")
    print(f"Destination: {test1.mission_name}")
    print(f"Duration: {test1.duration_days} days")
    print(f"Budget: ${test1.budget_millions:}M")
    print(f"Crew size: {len(test1.crew)}")
    for i in test1.crew:
        print(f"- {i.name} ({i.rank.value}) - {i.specialization}")

    print("\n=========================================")
    try:
        print("Expected validation error:")
        test1 = SpaceMission(
            mission_id="I2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500.0,
            launch_date=datetime.fromisoformat("2026-03-07T19:38"),
            crew=[
                CrewMember(
                    member_id="SC001",
                    name="Sarah Connor",
                    rank=RankEnum.captain,
                    age=35,
                    specialization="Mission Command",
                    years_experience=1,
                    is_active=True
                ),
                CrewMember(
                    member_id="SC002",
                    name="John Smith",
                    rank=RankEnum.cadet,
                    age=20,
                    specialization="Navigation",
                    years_experience=1,
                    is_active=True
                ),
                CrewMember(
                    member_id="SC003",
                    name="Alice Johnson",
                    rank=RankEnum.cadet,
                    age=18,
                    specialization="Engineering",
                    years_experience=1,
                    is_active=True
                )
            ]
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"Error: {error['msg']}")


if __name__ == "__main__":
    main()
