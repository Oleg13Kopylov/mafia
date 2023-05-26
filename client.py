import asyncio
import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc

from time import sleep
import signal
import os

class Player:
    def __init__(self):
        self.game_in_progress = False
        self.room_number = -1
        self.channel = 'localhost:12345'
        self.stub = mafia_pb2_grpc.MafiaServerStub(grpc.aio.insecure_channel(self.channel))
        self.name = 'not_set'
        self.role_in_game = 'not_set'
        self.wants_to_leave = False
        self.can_start_game = False
        self.is_alive = True
        self.is_night = False
        self.is_day = False


    async def GetRoomId(self):
        response = await self.stub.GetRoomId(mafia_pb2.request_room_id())
        self.room_number = response.room_id
        print("Room number set!", self.room_number)


    async def TryToSetName(self):
        print("Print your name:")
        while True:
            name = input()
            response_result = await self.stub.SetUserName(mafia_pb2.request_to_join(name=name, room_id=self.room_number))
            if not response_result.ans_bool:
                print("Try a different name! This one is already taken! Sorry!")
            else:
                self.name = name
                break


    async def WaitForGameToStart(self):
        print("Please, be patient. Waiting for other users to join the room.")
        response = await self.stub.InformThatGameHasStarted(mafia_pb2.has_game_started(room_id=self.room_number))
        while not response.ans_bool:
            sleep(1)
            response = await self.stub.InformThatGameHasStarted(mafia_pb2.has_game_started(room_id=self.room_number))
        print("Hurray! The game has begun!")


    async def TellThatAreReadyToStart(self):
        while True:
            await asyncio.sleep(1)
            if self.can_start_game:
                break

        response = await self.stub.PrescribeRole(mafia_pb2.request_to_get_role(name=self.name, room_id=self.room_number))
        self.role_in_game = response.str
        print("\nYour role is", self.role_in_game)
        day_number = 0
        while True:
            await self.CheckIfGameIsFinished()
            print()
            await asyncio.sleep(1)
            response = await self.stub.StartDay(mafia_pb2.request_to_start_day(name=self.name, room_id=self.room_number))
            day_number = response.int
            self.is_night = False
            self.is_day = True
            # print('New day number ' + str(response.int)  + ' started!')
            while True:
                await asyncio.sleep(1)
                print("\nNow it is day number " + str(response.int) + " in progress.")
                if self.is_alive:
                    res = input('If you would like to end it, type "y": ')
                    if res == 'y':
                        await asyncio.sleep(1)
                        print('Please, wait, we are waiting for other players to end the day...')
                        second_response = await self.stub.WantToEndDay(mafia_pb2.request_to_end_day(name=self.name, room_id=self.room_number))
                        self.is_day = False
                        break
                else:
                    print("You were killed earlier, and you are a ghost now.")
                    print("So we do now ask you to end day.")
                    print('Please, wait, we are waiting for other players to end the day...')
                    second_response = await self.stub.WantToEndDay(
                        mafia_pb2.request_to_end_day(name=self.name, room_id=self.room_number))
                    self.is_day = False
                    break
            # Если игрок не жив, то никаких действий он не выполняет
            await asyncio.sleep(1)
            third_response = await self.stub.GetAliveUserNames(mafia_pb2.request_to_get_alive_users(room_id=self.room_number))
            print(third_response.str)

            if day_number == 1:
                print("This is the first day, so today we are not executing anyone.")
            else:
                ### VOTING BEGIN
                if self.is_alive:
                    print("Now it is time to decide which player you want to execute at the end of day.")
                    while True:
                        name_to_execute = input('Type the name of the player that you want to execute: ')
                        print("Please, wait for others to choose whom they want to execute...")
                        response_execute = await self.stub.ExecutePlayer(mafia_pb2.request_to_execute(name=name_to_execute, room_id=self.room_number, is_ghost=False))
                        if response_execute.validity:
                            print("\nNEWS: The town collectively decided to execute", response_execute.name_of_executed)
                            if response_execute.name_of_executed == self.name:
                                self.is_alive = False
                            break
                        else:
                            print("You typed the wrong name, please try again.")
                else:
                    print("You were killed earlier, and you are a ghost now.")
                    print("So we do now ask you to choose to person to be executed at the end of the day.")
                    print('Please, wait, we are waiting for other players to choose\nthe person to be executed at the end of the day...')
                    response_execute_for_ghost = await self.stub.ExecutePlayer(
                        mafia_pb2.request_to_execute(name="NO ONE", room_id=self.room_number, is_ghost=True))
            await self.CheckIfGameIsFinished()
            response_ = await self.stub.StartNight(
                mafia_pb2.request_to_start_night(name=self.name, room_id=self.room_number))
            print("\nNow it is night number " + str(response.int) + " in progress.")
            self.is_night = True
            self.is_day = False
            if self.is_alive:
                print("Your name is ", self.name)
                print("You are alive!")
                # в зависимости от роли выполняется действие
                if self.role_in_game == 'mafia':
                    print("Your role is mafia, so you kill someone at night.\n")
                    while True:
                        res = input('Type the name of the person that you wanna kill: ')
                        response_on_killing = await self.stub.KillPerson(mafia_pb2.request_to_kill(name=res, room_id=self.room_number))
                        if response_on_killing.ans_bool:
                            break
                        else:
                            print("You typed the wrong name, please try again.")
                elif self.role_in_game == 'commissar':
                    print("Your role is commissar, so you check if someone is mafia.\nChoose the person to check:")
                    while True:
                        res = input('Type the name of the person that you wanna check: ')
                        response_on_checking = await self.stub.CheckPerson(mafia_pb2.request_to_check(name=res, room_id=self.room_number))
                        if response_on_checking.validity:
                            if response_on_checking.ans:
                                print("Yes, the person with name", res, 'IS mafia.')
                                flag_to_break = False
                                while True:
                                    user_input = input('Would you like to publish this info? Type "y" or "n" : ')
                                    if user_input == 'y':
                                        flag_to_break = True
                                        response_on_publishing = await self.stub.RevealThatPersonIsMafia(
                                            mafia_pb2.request_to_publish(name=res, room_id=self.room_number))
                                        print("You decided to publish that", res, 'is mafia.')
                                        break
                                    elif user_input == 'n':
                                        flag_to_break = True
                                        print("You decided NOT to publish that", res, 'is mafia.')
                                        break
                                    else:
                                        print("You typed the wrong reply, please try again.")
                                if flag_to_break:
                                    break
                            else:
                                print("No, the person with name ", res, 'is NOT mafia.')
                                break
                        else:
                            print("This person is NOT in the room, please try again.")


                elif self.role_in_game == 'citizen':
                    print("Your role is citizen, so you sleep at night...")
                else:
                    print("UNKNOWN ROLE!!!")
                    exit(1)
            else:
                print("You were killed earlier, so now you are a ghost.\nYou don't do anything at night.")

            print('Please, wait, we are waiting for other players to end the night...')
            await self.stub.WantToEndNight(mafia_pb2.request_to_end_night(name=self.name, room_id=self.room_number))
            await asyncio.sleep(1)


    async def GetUpdatesOnGameProcessFromServer(self):
        async for response in self.stub.GetUpdatesOnGameProcessFromServer(mafia_pb2.request_updates(name=self.name, room_id=self.room_number)):
            event_type = response.event_type
            message = response.message
            if event_type == 2:  # игра началась
                self.can_start_game = True
                print(message,)
            elif event_type == -1:
                name_of_killed_person = message.split()[0]
                ## Если ночь, то подождать, пока не публиковать.
                ## для коммиссара замутить то же самое
                while self.is_night:
                    await asyncio.sleep(1)
                print("NEWS:", message)
                if name_of_killed_person == self.name:
                    self.is_alive = False
                    print("You were killed :(")
            elif event_type == -2:
                while self.is_night:
                    await asyncio.sleep(1)
                print(message)
            else:
                print(message)


    async def CheckIfGameIsFinished(self):
        response = await self.stub.CheckIfGameIsFinished(mafia_pb2.check_if_game_is_finished_request(room_id=self.room_number))
        ans_bool, ans_str = response.ans_bool, response.ans_str
        if ans_bool:
            print(ans_str)
            os._exit(1)


    async def Leave(self):
        # print("FROM LEAVE")
        while not self.wants_to_leave:
            await asyncio.sleep(1)
        await self.stub.InformThatUserHasLeft(mafia_pb2.request_to_leave(name=self.name, room_id=self.room_number))


global_this_player_for_handler = None


async def handler(signum):
    res = input('Ctrl-c was pressed. Do you really mean to exit? Type "y" or "n" : ')
    if res == 'y':
        if global_this_player_for_handler is not None:
            print('Leaving')
            global_this_player_for_handler.wants_to_leave = True
            await global_this_player_for_handler.Leave()
            print('You have left the game.')
            os._exit(0)

    print('You changed your opinion and you are still in the game')


signal.signal(signal.SIGINT, handler)


async def run() -> None:
    this_player = Player()
    global global_this_player_for_handler
    global_this_player_for_handler = this_player
    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                lambda: asyncio.ensure_future(handler(signame)))
    await this_player.GetRoomId()
    await this_player.TryToSetName()

    WaitForGameToStart_And_GetUpdatesOnGameProcessFromServer_And_TellThatAreReadyToStart = [
        this_player.WaitForGameToStart(),
        this_player.GetUpdatesOnGameProcessFromServer(),
        this_player.TellThatAreReadyToStart()
    ]
    await asyncio.gather(*WaitForGameToStart_And_GetUpdatesOnGameProcessFromServer_And_TellThatAreReadyToStart)
    await this_player.TellThatAreReadyToStart()


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
