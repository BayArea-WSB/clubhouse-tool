import os
import sys
import keyboard
from clubhouse.clubhouse import Clubhouse

CLUBHOUSE_PHONENUMBER = os.environ.get("CLUBHOUSE_PHONENUMBER")

AWSB_CHANNEL_NAME = "M1wvbqK1"
AWSB_CLUB_ID = "2081718418"


class AuthException(Exception):
    def __init__(self, message=None):
        self.message = message


def get_member_usernames(users):
    usernames = []
    for u in users:
        usernames.append(u["username"])

    return usernames


class ClubhouseUtil:
    def __init__(self, phone=CLUBHOUSE_PHONENUMBER):
        self.client = Clubhouse()
        self.phone = phone
        self.user_authentication()

    def authenticated(self):
        user_id = os.environ.get("CLUBHOUSE_USER_ID")
        user_token = os.environ.get("CLUBHOUSE_USER_TOKEN")
        user_device = os.environ.get("CLUBHOUSE_USER_DEVICE")

        if user_id and user_token and user_device:
            self.client = Clubhouse(
                user_id=user_id, user_token=user_token, user_device=user_device
            )
            return True
        else:
            return False

    def user_authentication(self):
        if self.authenticated():
            return

        result = self.client.start_phone_number_auth(self.phone)
        if not result["success"]:
            err_msg = (
                f"[-] Error occured during authentication. ({result})"
            )
            raise AuthException(err_msg)

        verification_code = input(f"Enter the {self.phone} SMS code: > ")
        result = self.client.complete_phone_number_auth(self.phone, verification_code)
        if not result["success"]:
            err_msg = (
                f"[-] Error occured during authentication. ({result['error_message']})"
            )
            raise AuthException(err_msg)

        if "user_profile" not in result:
            print(result)
            sys.exit(1)

        user_id = result["user_profile"]["user_id"]
        user_token = result["auth_token"]
        user_device = self.client.HEADERS.get("CH-DeviceId")

        print("Run command local")
        print(
            f"heroku config:set CLUBHOUSE_USER_ID={user_id} CLUBHOUSE_USER_TOKEN={user_token} CLUBHOUSE_USER_DEVICE={user_device}"
        )
        return

    def check_members(self, usernames):
        res = self.client.get_club_members(
            AWSB_CLUB_ID, return_members=True, page_size=99999999999, page=1
        )
        if "users" not in res:
            err = res
            raise AuthException(err_msg)

        all_members = set(get_member_usernames(res["users"]))

        input_usernames = set(usernames)

        no_members = input_usernames - all_members
        members = input_usernames - no_members

        data = {
            "members": list(members),
            "no_members": list(no_members),
        }
        return data


if __name__ == "__main__":
    if CLUBHOUSE_PHONENUMBER is None:
        print("Please config CLUBHOUSE_PHONENUMBER in env")
        sys.exit(1)

    ClubhouseUtil()
    # import pdb; pdb.set_trace()
    # cu.check_members(['michael0o0', 'amy', 'bugfree'])
