import random
import asyncio
from asyncio import Condition
import logging
from typing import Any, Coroutine

import grpc
import mafia_pb2
import mafia_pb2_grpc
import random
from time import sleep
import sys
import os

NUM_OF_ROOMS = 12345
NUM_OF_PLAYERS_TO_START = 4


class PlayRoom():
    def __init__(self):
        self.players_names = list()
        self.event_history = list()
        self.event_index_to_name_to_message = dict()
        self.event_to_message_to_all = list()
        self.game_started = False
        self.position_to_role = self.generate_mapping_from_position_to_role()
        self.day_number = 0
        self.position_to_aliveness = [True] * NUM_OF_PLAYERS_TO_START
        self.user_to_be_checked = None
        self.user_to_be_killed_by_society = None
        self.user_to_be_killed_by_mafia = None
        self.position_to_wants_to_start_day = [True] * NUM_OF_PLAYERS_TO_START
        self.day_is_started = False
        self.night_is_started = False
        self.position_to_has_day_started_for_user = [False] * NUM_OF_PLAYERS_TO_START
        self.position_to_has_night_started_for_user = [False] * NUM_OF_PLAYERS_TO_START
        self.position_to_wants_to_end_day = [False] * NUM_OF_PLAYERS_TO_START
        self.position_to_wants_to_end_night = [False] * NUM_OF_PLAYERS_TO_START
        self.position_to_wants_to_start_night = [False] * NUM_OF_PLAYERS_TO_START
        self.position_to_num_of_execution_votes = [0] * NUM_OF_PLAYERS_TO_START
        self.person_to_execute = None
        self.game_is_finished = False


    def generate_mapping_from_position_to_role(self):
        d = [''] * 4
        mafia_rand_pos = random.randint(0, 3)
        d[mafia_rand_pos] = 'mafia'
        commissar_rand_pos = random.randint(0, 3)
        while commissar_rand_pos == mafia_rand_pos:
            commissar_rand_pos = random.randint(0, 3)
        d[commissar_rand_pos] = 'commissar'
        for i in range(4):
            if d[i] == '':
                d[i] = 'citizen'
        return d

    def add_user(self, name_of_user):
        self.players_names.append(name_of_user)

    def get_num_of_players(self):
        return len(self.players_names)

    def get_role_for_player(self, name):
        position = self.players_names.index(name)
        return self.position_to_role[position]

    def get_event_history(self, index):
        return self.event_history[index]

    def get_message(self, event_index, name):
        return self.event_to_message_to_all[event_index]  + self.event_index_to_name_to_message.get(event_index, {}).get(name, '')

    def add_event_and_message_to_all(self, event_type, message):
        self.event_history.append(event_type)
        self.event_to_message_to_all.append(message)

    def get_len_of_events(self):
        return len(self.event_history)

    def start_game_in_room(self):
        if not self.game_started:
            self.add_event_and_message_to_all(2, 'The game has just started!')
            self.game_started = True

    def get_aliveness_for_player(self, name):
        position = self.players_names.index(name)
        return self.position_to_aliveness[position]

    def get_wants_to_start_day_for_player(self, name):
        position = self.players_names.index(name)
        return self.position_to_wants_to_start_day[position]

    def get_wants_to_start_night_for_player(self, name):
        position = self.players_names.index(name)
        return self.position_to_wants_to_start_night[position]

    def check_that_all_wanna_start_the_day(self):
        for name in self.players_names:
            if not self.get_wants_to_start_day_for_player(name):
                return False
        if not self.day_is_started:
            self.day_is_started = True
            self.night_is_started = False
            self.day_number += 1
            self.position_to_wants_to_end_day = [False] * NUM_OF_PLAYERS_TO_START
            # self.add_event_and_message_to_all(4, '\nDay number ' + str(self.day_number) + ' just started!')
        return True

    def check_that_all_wanna_start_the_night(self):
        for name in self.players_names:
            if not self.get_wants_to_start_night_for_player(name):
                return False
        if not self.night_is_started:
            self.day_is_started = False
            self.night_is_started = True
            self.position_to_wants_to_end_night = [False] * NUM_OF_PLAYERS_TO_START
            # self.add_event_and_message_to_all(7, '\nNight number ' + str(self.day_number) + ' just started!')
        return True

    def get_day_number(self):
        return self.day_number

    def get_has_day_started_for_player(self, name):
        position = self.players_names.index(name)
        return self.position_to_has_day_started_for_user[position]

    def start_day_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_has_day_started_for_user[position] = True
        self.position_to_wants_to_end_day[position] = False
        self.position_to_has_night_started_for_user[position] = False

    def start_night_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_has_day_started_for_user[position] = False
        self.position_to_has_night_started_for_user[position] = True

    def set_wants_to_end_day_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_wants_to_end_day[position] = True

    def set_wants_to_end_night_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_wants_to_end_night[position] = True

    def set_wants_to_start_night(self, name):
        position = self.players_names.index(name)
        self.position_to_wants_to_start_night[position] = True

    def set_wants_to_start_day(self, name):
        position = self.players_names.index(name)
        self.position_to_wants_to_start_day[position] = True

    def check_that_all_wanna_end_the_day(self):
        for name in self.players_names:
            position = self.players_names.index(name)
            if not self.position_to_wants_to_end_day[position]:
                return False
        if not self.night_is_started:
            self.night_is_started = True
            self.day_is_started = False
            # self.add_event_and_message_to_all(5, 'Day number ' + str(self.day_number) + ' just ended!')
            self.position_to_wants_to_start_day = [False] * NUM_OF_PLAYERS_TO_START
            self.position_to_wants_to_end_night = [False] * NUM_OF_PLAYERS_TO_START
        return True

    def check_that_all_wanna_end_the_night(self):
        for name in self.players_names:
            position = self.players_names.index(name)
            if not self.position_to_wants_to_end_night[position]:
                return False
        if not self.day_is_started:
            self.night_is_started = False
            self.day_is_started = True
            # self.add_event_and_message_to_all(6, 'Night number ' + str(self.day_number) + ' just ended!')
            self.day_number += 1
            self.position_to_wants_to_start_day = [False] * NUM_OF_PLAYERS_TO_START
            self.position_to_wants_to_start_night = [False] * NUM_OF_PLAYERS_TO_START
        return True

    def end_day_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_has_day_started_for_user[position] = False
        self.position_to_has_night_started_for_user[position] = True

    def end_night_for_user(self, name):
        position = self.players_names.index(name)
        self.position_to_has_day_started_for_user[position] = True
        self.position_to_has_night_started_for_user[position] = False

    def get_player_names(self):
        return self.players_names

    def get_alive_players_names(self):
        ans_to_return = []
        for name in self.get_player_names():
            if self.get_aliveness_for_player(name):
                ans_to_return.append(name)
        return ans_to_return

    def kill_person_with_name(self, name):
        if name not in self.players_names:
            return False
        if not self.get_aliveness_for_player(name):
            return False
        self.position_to_aliveness[self.players_names.index(name)] = False
        return True

    def check_person_with_name(self, name):
        return ('mafia' == self.get_role_for_player(name))

    def see_if_player_exists(self, name):
        return (name in self.players_names)

    def set_wants_to_execute(self, name):
        position = self.players_names.index(name)
        self.position_to_num_of_execution_votes[position] += 1

    def check_that_all_wanna_execute(self):
        num_votes = 0
        for el in self.position_to_num_of_execution_votes:
            num_votes += el
        return (len(self.get_alive_players_names()) <= num_votes)

    def get_name_of_person_to_execute(self):
        if self.person_to_execute is None:
            maxim = max(self.position_to_num_of_execution_votes)
            persons_with_maxim_votes = []
            for name in self.players_names:
                position = self.players_names.index(name)
                if self.position_to_num_of_execution_votes[position] == maxim:
                    persons_with_maxim_votes.append(name)
            chosen = random.choice(persons_with_maxim_votes)
            self.person_to_execute = chosen
        return self.person_to_execute

    def execute_person_with_name(self, name):
        position = self.players_names.index(name)
        self.position_to_aliveness[position] = False

    def set_person_to_execute_to_none(self):
        self.person_to_execute = None
        self.position_to_num_of_execution_votes = [0] * NUM_OF_PLAYERS_TO_START

    def get_num_of_mafia(self):
        count = 0
        for position in range(len(self.position_to_role)):
            role = self.position_to_role[position]
            if self.position_to_aliveness[position] and (role == 'mafia'):
                count += 1
        return count

    def get_num_of_rightful_people(self):
        count = 0
        for position in range(len(self.position_to_role)):
            role = self.position_to_role[position]
            if self.position_to_aliveness[position] and (role != 'mafia'):
                count += 1
        return count

    def check_if_game_is_finished(self):
        ans = False
        str = ''
        if self.get_num_of_mafia() == 0:
            ans = True
            str = '\n\nTHE END: Rightful(peaceful) people/citizens have won!\n\n'
        elif self.get_num_of_mafia() >= self.get_num_of_rightful_people():
            ans = True
            str = '\n\nTHE END: Mafia have won!\n\n'
        return [ans, str]

    def has_game_started(self):
        return self.game_started

    def remove_user_from_room(self, name):
        position = self.players_names.index(name)
        self.players_names[position], self.players_names[-1] = self.players_names[-1], self.players_names[position]
        self.players_names.pop()



class Server(mafia_pb2_grpc.MafiaServer):
    def __init__(self):
        self.active_rooms_numbers = set()
        self.free_rooms_numbers = set()
        for i in range(1, NUM_OF_ROOMS + 1):
            self.free_rooms_numbers.add(i)
        self.not_full_room_number = -1
        self.cur_num_of_players_in_not_full_room = 0
        self.room_number_to_room = dict()

    def add_user_to_room(self, name, room_number):
        self.room_number_to_room[room_number].add_user(name)

    def get_num_of_players_in_room_number(self, room_number):
        return self.room_number_to_room[room_number].get_num_of_players()

    async def GetRoomId(self, request, context):  # TODO: CHECK
        if self.not_full_room_number == -1:  # Нет комнаты, которая заполнена частично (в эту комнату ждем игроков).
            # Надо подобрать новую комнату
            if len(self.free_rooms_numbers) == 0:
                print("No rooms available! Exiting!")
                sys.exit()
            else:
                room_number_to_give = self.free_rooms_numbers.pop()
                self.cur_num_of_players_in_not_full_room = 1
                self.room_number_to_room[room_number_to_give] = PlayRoom()
                self.not_full_room_number = room_number_to_give
                return mafia_pb2.reply_room_id(room_id=room_number_to_give)
        # Есть комната, заполненная частично
        room_number_to_give = self.not_full_room_number
        self.cur_num_of_players_in_not_full_room += 1
        if self.cur_num_of_players_in_not_full_room == 4:
            # В комнате стало нужное число игроков. Теперь нет не полностью заполненной комнаты
            self.cur_num_of_players_in_not_full_room = 0
            self.not_full_room_number = -1
        return mafia_pb2.reply_room_id(room_id=room_number_to_give)

    async def SetUserName(self, request, context, **kwargs):
        if request.name in self.room_number_to_room[request.room_id].players_names:
            print("This name is already taken!")
            return mafia_pb2.reply_bool(ans_bool=False)
        self.add_user_to_room(request.name, request.room_id)
        print(request.name + " joined!")
        self.room_number_to_room[request.room_id].add_event_and_message_to_all(1, 'User ' + request.name + ' joined the room!')
        # 1 – присоединился пользователь
        return mafia_pb2.reply_bool(ans_bool=True)

    async def InformThatGameHasStarted(self, request, context, **kwargs):
        room_id = request.room_id
        print('There are', self.get_num_of_players_in_room_number(room_id), 'out of', NUM_OF_PLAYERS_TO_START,
              'in the room')
        if (NUM_OF_PLAYERS_TO_START > self.get_num_of_players_in_room_number(room_id)):

            return mafia_pb2.reply_bool(ans_bool=False)
        self.room_number_to_room[request.room_id].start_game_in_room()
        # 2 – игра началась
        # print('Leaving InformThatGameHasStarted')
        return mafia_pb2.reply_bool(ans_bool=True)

    async def PrescribeRole(self, request, context):
        room_number = request.room_id
        name_of_user = request.name
        role = self.room_number_to_room[room_number].get_role_for_player(name_of_user)
        return mafia_pb2.reply_str(str=role)

    async def GetUpdatesOnGameProcessFromServer(self, request, context):
        cur_event_index = 0
        cur_room = self.room_number_to_room[request.room_id]
        while True:
            if cur_event_index < cur_room.get_len_of_events():

                yield mafia_pb2.reply_event(event_type=cur_room.get_event_history(cur_event_index),
                                            message=cur_room.get_message(cur_event_index, request.name))
                cur_event_index += 1
            else:
                await asyncio.sleep(1)


    async def InformThatUserHasLeft(self, request, context):
        name = request.name
        room_id = request.room_id
        if room_id != -1:
            self.room_number_to_room[request.room_id].add_event_and_message_to_all(3, 'User ' + name + ' left the room')
            if self.room_number_to_room[request.room_id].has_game_started():
                self.room_number_to_room[request.room_id].kill_person_with_name(name)
            else:
                self.cur_num_of_players_in_not_full_room -= 1
                self.room_number_to_room[request.room_id].remove_user_from_room(name)

        # 3 – пользователь отключился
        # print('Leaving InformThatGameHasStarted')
        return mafia_pb2.empty_reply()


    async def StartDay(self, request, context):
        room_id = request.room_id
        while True:
            if self.room_number_to_room[room_id].check_that_all_wanna_start_the_day():
                self.room_number_to_room[room_id].set_person_to_execute_to_none()
                self.room_number_to_room[room_id].start_day_for_user(request.name)
                return mafia_pb2.reply_int(int=self.room_number_to_room[room_id].get_day_number())
            else:
                await asyncio.sleep(1)
            # print("Day")

    async def StartNight(self, request, context):
        room_id = request.room_id
        while True:
            if self.room_number_to_room[room_id].check_that_all_wanna_start_the_night():
                self.room_number_to_room[room_id].start_night_for_user(request.name)
                return mafia_pb2.reply_int(int=self.room_number_to_room[room_id].get_day_number())
            else:
                await asyncio.sleep(1)
            # print("Night")

    async def WantToEndDay(self, request, context):
        name = request.name
        room_id = request.room_id
        self.room_number_to_room[room_id].set_wants_to_end_day_for_user(name)
        while True:
            if self.room_number_to_room[room_id].check_that_all_wanna_end_the_day():
                self.room_number_to_room[room_id].end_day_for_user(request.name)
                self.room_number_to_room[room_id].set_wants_to_start_night(request.name)
                return mafia_pb2.reply_int(int=self.room_number_to_room[room_id].get_day_number())
            else:
                await asyncio.sleep(1)

    async def GetAliveUserNames(self, request, context):
        room_id = request.room_id
        lst_of_alive_players = self.room_number_to_room[room_id].get_alive_players_names()
        ans = "\nThere are " + str(len(lst_of_alive_players)) + ' alive users:\n' + '\n'.join(lst_of_alive_players)
        return mafia_pb2.reply_str(str=ans)

    async def KillPerson(self, request, context):
        room_id = request.room_id
        name_to_kill = request.name
        my_bool = self.room_number_to_room[room_id].kill_person_with_name(name_to_kill)
        if my_bool:
            self.room_number_to_room[room_id].add_event_and_message_to_all(-1, name_to_kill + ' was killed!')
        return mafia_pb2.reply_bool(ans_bool=my_bool)

    async def WantToEndNight(self, request, context):
        name = request.name
        room_id = request.room_id
        self.room_number_to_room[room_id].set_wants_to_end_night_for_user(name)
        while True:
            if self.room_number_to_room[room_id].check_that_all_wanna_end_the_night():
                self.room_number_to_room[room_id].end_night_for_user(request.name)
                self.room_number_to_room[room_id].set_wants_to_start_day(request.name)
                return mafia_pb2.reply_int(int=self.room_number_to_room[room_id].get_day_number())
            else:
                await asyncio.sleep(1)

    async def CheckPerson(self, request, context):
        room_id = request.room_id
        name_to_check = request.name
        my_validity = self.room_number_to_room[room_id].see_if_player_exists(name_to_check)
        if my_validity:
            my_bool = self.room_number_to_room[room_id].check_person_with_name(name_to_check)
        else:
            my_bool = False

        return mafia_pb2.reply_check(validity=my_validity, ans=my_bool)

    async def RevealThatPersonIsMafia(self, request, context):
        room_id = request.room_id
        name_to_reveal = request.name
        if self.room_number_to_room[room_id].get_role_for_player(name_to_reveal) != 'mafia':
            print("Something went wrong with commissar's interaction with server!")
            exit(1)
        self.room_number_to_room[room_id].add_event_and_message_to_all(-2,
                                                                       "NEWS: The commissar has found that " +
                                                                       name_to_reveal + ' is mafia!')
        return mafia_pb2.reply_bool(ans_bool=True)

    async def ExecutePlayer(self, request, context):
        if not request.is_ghost:
            room_id = request.room_id
            name_to_execute = request.name
            if name_to_execute not in self.room_number_to_room[room_id].get_alive_players_names():
                return mafia_pb2.response_to_execute(validity=False, name_of_executed="WRONG_NAME")
            self.room_number_to_room[room_id].set_wants_to_execute(name_to_execute)
            while True:
                if self.room_number_to_room[room_id].check_that_all_wanna_execute():
                    person_executed = self.room_number_to_room[room_id].get_name_of_person_to_execute()
                    self.room_number_to_room[room_id].execute_person_with_name(person_executed)
                    return mafia_pb2.response_to_execute(validity=True, name_of_executed=person_executed)
                else:
                    await asyncio.sleep(1)
        else:
            room_id = request.room_id
            while True:
                if self.room_number_to_room[room_id].check_that_all_wanna_execute():
                    person_executed = self.room_number_to_room[room_id].get_name_of_person_to_execute()
                    self.room_number_to_room[room_id].execute_person_with_name(person_executed)
                    return mafia_pb2.response_to_execute(validity=True, name_of_executed=person_executed)
                else:
                    await asyncio.sleep(1)

    async def CheckIfGameIsFinished(self, request, context):
        room_id = request.room_id
        ans_bool, ans_str = self.room_number_to_room[room_id].check_if_game_is_finished()
        return mafia_pb2.check_if_game_is_finished_reply(ans_bool=ans_bool, ans_str=ans_str)


async def serve() -> None:
    server = grpc.aio.server()
    mafia_pb2_grpc.add_MafiaServerServicer_to_server(Server(), server)
    listen_addr = '[::]:12345'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
