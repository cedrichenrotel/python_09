# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  alien_contact.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/06 18:52:15 by cehenrot        #+#    #+#               #
#  Updated: 2026/04/07 14:47:30 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
try:
    from datetime import datetime
    from typing import Optional
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from enum import Enum
except ImportError as e:
    print(e)
    sys.exit(1)


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def CustomValidationRules(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError("[WARNING] -> contact_id does not begin with "
                             "'AC'")
        elif (self.contact_type == ContactType.physical and
              self.is_verified is False):
            raise ValueError("[WARNING] -> Reports of physical contact that "
                             "have not been verified")
        elif (self.witness_count < 3 and
              self.contact_type == ContactType.telepathic):
            raise ValueError("[WARNING] -> Telepathic contact requires at "
                             "least 3 witnesses")
        elif (self.signal_strength > 7.0 and
              self.message_received is None):
            raise ValueError("[WARNING] -> signal strength greater than 7.0")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    try:
        test1 = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-04-06T16:30"),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greetings from Zeta Reticuli',
            is_verified=True
         )
    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error: {error['msg']}")
        sys.exit(1)

    print(f"ID: {test1.contact_id}")
    print(f"Type: {test1.timestamp}")
    print(f"Location: {test1.location}")
    print(f"Signal: {test1.signal_strength}/10")
    print(f"Duration: {test1.duration_minutes} minutes")
    print(f"Witnesses: {test1.witness_count}")
    print(f"Message: {test1.message_received}")

    print("\n======================================")
    print("Invalid contact report:")
    try:
        test2 = AlienContact(
           contact_id="AC_2024_001",
           timestamp=datetime.fromisoformat("2026-04-06T16:30"),
           location="Area 51, Nevada",
           contact_type=ContactType.physical,
           signal_strength=9,
           duration_minutes=45,
           witness_count=2,
           message_received=None,
           is_verified=False
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error: {error['msg']}")
        return

    print(f"ID: {test2.contact_id}")
    print(f"Type: {test2.timestamp}")
    print(f"Location: {test2.location}")
    print(f"Signal: {test2.signal_strength}/10")
    print(f"Duration: {test2.duration_minutes} minutes")
    print(f"Witnesses: {test2.witness_count}")
    print(f"Message: {test2.message_received}")


if __name__ == "__main__":
    main()
