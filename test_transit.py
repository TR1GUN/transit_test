# здесь расположим тестовые прогоны транзита

import pytest
# from conftest import run_up_server_tcp

# -------------------------------------------------------------------------------------------------------------------
#                                        Сервисные функции
# -------------------------------------------------------------------------------------------------------------------
# @pytest.fixture(scope="function")
# def run_up_server_tcp():
#     from RunUpServer.Run_Up_Server import RunUpServer
#     # Подымаем сервер
#     ServerSettings = RunUpServer(rtu327=False, iface1=True, iface2=True, iface3=False, iface4=True)
#     print('Сервер Подняли...')
#     # return ServerSettings


def parametrize(parametrize_dict: list):
    """
    Функция для прикручивания параметров

    """
    parametrs = []
    for i in parametrize_dict:
        line_parametrs = list(i.values())
        # line_parametrs =  line_parametrs + [run_up_server_tcp]
        #
        # print(run_up_server_tcp)

        line_parametrs = tuple(line_parametrs)
        # if len(line_parametrs) == 1:
        #     line_parametrs = line_parametrs[0]
        parametrs.append(line_parametrs)
    return parametrs


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Отправляем на TCP читаем COM
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
parametrize_TCPtoCOM = [
    {
        'data': 'Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_МирВойна_и_Мир_Война_и_Мир_Война_и_Мир ',
        'COM': 'COM1',
    },
    {
        'data': 'Are you really a programmer or are you just pretending?',
        'COM': 'COM1',
    },
    {
        'data': '1010',
        'COM': 'COM2',
    },
    {
        'data': 'На словах ты Лев Толстой, а каков ты в деле?',
        'COM': 'COM2',
    },
    {
        'data': 'Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир_Война_и_Мир',
        'COM': 'COM3',
    },
    {
        'data': 'На словах ты Лев Толстой, а каков ты в деле?',
        'COM': 'COM3',
    },
    {
        'data': """
[Intro]
"Look, I was gonna go easy on you not to hurt your feelings"
"But I'm only going to get this one chance" (Six minutes— Six minutes—)
"Something's wrong, I can feel it" (Six minutes, Slim Shady, you're on!)
"Just a feeling I've got, like something's about to happen, but I don't know what. 
If that means what I think it means, we're in trouble, big trouble; 
And if he is as bananas as you say, I'm not taking any chances"
"You are just what the doc ordered"

[Chorus]
I'm beginnin' to feel like a Rap God, Rap God
All my people from the front to the back nod, back nod
Now, who thinks their arms are long enough to slap box, slap box?
They said I rap like a robot, so call me Rap-bot

[Verse 1]
But for me to rap like a computer it must be in my genes
I got a laptop in my back pocket
My pen'll go off when I half-cock it
Got a fat knot from that rap profit
Made a livin' and a killin' off it
Ever since Bill Clinton was still in office
With Monica Lewinsky feelin' on his nutsack
I'm an MC still as honest
But as rude and as indecent as all hell
Syllables, skill-a-holic (Kill 'em all with)
This flippity dippity-hippity hip-hop
You don't really wanna get into a pissin' match
With this rappity brat, packin' a MAC in the back of the Ac'
Backpack rap crap, yap-yap, yackety-yack
And at the exact same time, I attempt these lyrical acrobat stunts while I'm practicin' that
I'll still be able to break a motherfuckin' table
Over the back of a couple of faggots and crack it in half
Only realized it was ironic, I was signed to Aftermath after the fact
How could I not blow? All I do is drop F-bombs
Feel my wrath of attack
Rappers are havin' a rough time period, here's a maxi pad
It's actually disastrously bad for the wack
While I'm masterfully constructing this masterpièce

[Chorus]
'Cause I'm beginnin' to feel like a Rap God, Rap God
All my people from the front to the back nod, back nod
Now, who thinks their arms are long enough to slap box, slap box?
Let me show you maintainin' this shit ain't that hard, that hard
Everybody want the key and the secret to rap immortality like Ι have got

[Verse 2]
Well, to be truthful the blueprint's
Simply rage and youthful exuberance
Everybody loves to root for a nuisance
Hit the Earth like an asteroid
Did nothing but shoot for the Moon since (Pew!)
MCs get taken to school with this music
'Cause I use it as a vehicle to "bus the rhyme"
Now I lead a new school full of students
Me? I'm a product of Rakim
Lakim Shabazz, 2Pac, N.W.A, Cube, hey Doc, Ren
Yella, Eazy, thank you, they got Slim
Inspired enough to one day grow up, blow up and be in a position
To meet Run–D.M.C., induct them
Into the motherfuckin' Rock and Roll Hall of Fame
Even though I'll walk in the church and burst in a ball of flames
Only Hall of Fame I'll be inducted in is the alcohol of fame
On the wall of shame
You fags think it's all a game, 'til I walk a flock of flames
Off a plank and, tell me what in the fuck are you thinkin'?
Little gay-lookin' boy
So gay I can barely say it with a straight face, lookin' boy (Ha-ha!)
You're witnessin' a mass-occur
Like you're watching a church gathering take place, lookin' boy
"Oy vey, that boy's gay!"—that's all they say, lookin' boy
You get a thumbs up, pat on the back
And a "way to go" from your label every day, lookin' boy
Hey, lookin' boy! What you say, lookin' boy?
I get a "hell yeah" from Dre, lookin' boy
I'ma work for everything I have, never asked nobody for shit
Get outta my face, lookin' boy!
Basically, boy, you're never gonna be capable
Of keepin' up with the same pace, lookin' boy, 'cause""",
        'COM': 'COM4',
    },
    {
        'data': 'На словах ты Лев Толстой, а каков ты в деле?',
        'COM': 'COM4',
    },
    {
        'data': 'Are you really a programmer or are you just pretending? \n',
        'COM': 'COM4',
    },
]


@pytest.mark.parametrize("data, COM", parametrize(parametrize_TCPtoCOM))
def test_transit_TCPtoCOM(data, COM):

    from Transit_TCP_to_COM import TCPtoCOM
    from time import sleep
    TransitTCPtoCOM = TCPtoCOM(data=data).Setup(COM=COM)
    # sleep(5)

@pytest.mark.parametrize("data, COM", parametrize(parametrize_TCPtoCOM))
def test_transit_COMtoTCP(data, COM):

    from Transit_COM_to_TCP import COMtoTCP
    from time import sleep
    TransitCOMtoTCP = COMtoTCP(data=data).Setup(COM=COM)
    # sleep(5)