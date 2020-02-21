import discord
from discord.ext import commands
import time
import http.cookiejar as cookielib
import urllib.request
import re
import base64
from PIL import Image
from random import choice, randint, shuffle
import os

def average_color(path):
    img = Image.open(path).convert("RGB")
    pixels = img.load()
    x, y = img.size
    all_pixels = x * y
    r = g = b = 0
    for i in range(x):
        for j in range(y):
            r_new, g_new, b_new = pixels[i, j]
            r += r_new
            g += g_new
            b += b_new
    res = (r // all_pixels, g // all_pixels, b // all_pixels)
    return res


def string_from_hex(s):
    s = ''.join(s.split('%'))
    b = bytes.fromhex(s)
    return b.decode('utf-8')


def hex_from_string(s):
    b = s.encode('utf-8')
    h = b.hex()
    data = []
    for i in range(len(h)):
        if i % 2 == 1:
            data.append(h[i - 1:i + 1])
    res = '%' + '%'.join(data)
    return res


def search_by_url(image_path, num=3):
    downloaded_images = 0
    cj = cookielib.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')]

    content = opener.open(image_path).read()
    path = f'data/default.jpg'
    with open(path, 'wb') as file:
        file.write(content)

    google_path = 'http://images.google.com/searchbyimage?image_url=' + image_path
    source = opener.open(google_path).read()
    with open('test.html', mode='wb') as f:
        f.write(source)
    obj = re.findall(r'<input class="gLFyf gsfi".*? value="(.*?)".*?>', source.decode('utf-8'))
    #obj_colloc = re.findall('<span class="st">.*?<em>(.*?)</em>.*?</span>', source.decode('utf-8'))
    obj_colloc = re.findall('<h3 class="LC20lb DKV0Md">(.*?)</h3>', source.decode('utf-8'))
    obj_words = []
    for colloc in obj_colloc:
        obj_words.extend(colloc.strip().lower().split())
    obj_words = list(filter(lambda x: len(x) > 2 and x.isalpha(), obj_words))
    word_res = sorted([(obj_words.count(word), word) for word in obj_words], reverse=True)
    possible_obj = word_res[0][1]
    if not obj:
        obj = 'a random object'
    else:
        obj = obj[0]
        url_object = f"{' '.join(obj.split())}"
        url = f"https://www.google.ru/search?newwindow=1&hl=ru&authuser=0&tbm=isch&sxsrf=ALeKk02lB6Z7ikRIRQUry3iALjHOM4HOKA%3A1582189067236&source=hp&biw=1920&bih=937&ei=C0pOXpvmC-iprgSP94D4BA&q={hex_from_string(url_object)}&oq=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82&gs_l=img.3..0l10.2415.8971..9214...4.0..0.172.652.8j1......0....1..gws-wiz-img.....10..35i39j35i362i39.AQu6cv3Z0hE&ved=0ahUKEwjbl8XK4d_nAhXolIsKHY87AE8Q4dUDCAY&uact=5"
        try:
            # big images
            content = opener.open(url).read()
            with open('test.html', mode='wb') as f:
                f.write(content)
            image_urls = re.findall('<img .*?data-iurl="(.*?)" .*? />', content.decode('utf-8')[251599:])[1:]
            second = average_color('data/default.jpg')
            for i in range(num):
                t = list(str(int(time.time())) + str(randint(1000, 90000)))
                shuffle(t)
                shuffle(t)
                t = ''.join(t)
                if num >= len(image_urls) - 3:
                    break
                content = opener.open(image_urls[i]).read()
                path = f'data/{t}.jpg'
                with open(path, 'wb') as file:
                    file.write(content)
                first = average_color(path)
                delt = 30
                if abs(first[0] - second[0]) > delt or abs(first[1] - second[1]) > delt or abs(
                        first[2] - second[2]) > delt:
                    os.remove(path)
                else:
                    downloaded_images += 1
                    if downloaded_images >= num:
                        break
                    ratio = 2.
                    image = Image.open(path).convert("RGB")
                    w, h = image.size
                    image = image.resize((int(w * ratio), int(h * ratio)))
                    image.save(path)
            if downloaded_images < num:
                raise TypeError
        except (UnicodeEncodeError, TypeError):
            results = re.findall(r"var s='(.*?)'", source.decode('utf-8'))
            for i in results:
                t = list(str(int(time.time())) + str(randint(1000, 90000)))
                shuffle(t)
                shuffle(t)
                t = ''.join(t)

                coded_string = ''.join(i.split(r'\x')[0]).split(',')[1]
                path = f'data/{t}.jpg'
                with open(path, 'wb') as file:
                    file.write(base64.decodebytes(str.encode(coded_string) + b'=='))
                downloaded_images += 1
                if downloaded_images >= num:
                    break
                ratio = 2.
                image = Image.open(path).convert("RGB")
                w, h = image.size
                image = image.resize((int(w * ratio), int(h * ratio)))
                image.save(path)
        except BaseException as e:
            print('\n', e, '\n')
        finally:
            os.remove('data/default.jpg')
    return obj, possible_obj


predictions = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes — definitely', 'You may rely on it',
               'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', 'Reply hazy, try again',
               'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
               'Don’t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
shuffle(predictions)
questions = []
bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    print(f'log in')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def h(ctx):
    await ctx.send(
        "```Welcome! I'm Discord bot and I'm very glad to see you!\n Here are some usefil commands:\n>help - it's clear I suppose\n>ping - to check bot activity\n>new voice [or 'text'] <name> - to create new channel automatically\n>predict <question> - to get a prediction on early question\nsearch <url> <num> - get    num    of similar images. Also bot will probably guess.```")


@bot.command()
async def new(ctx, type, *name):
    name = '-'.join(name)
    if type == 'voice':
        chan_2 = await ctx.guild.create_voice_channel(name=name)
    elif type == 'text':
        chan = await ctx.guild.create_text_channel(name=name)
    else:
        await ctx.send("Invalid command (or you're) Use !help")
        return
    await ctx.send('New channel was created. Check it out now!')


@bot.command()
async def predict(ctx, *que):
    global questions
    req = ' '.join(que)
    if req in questions:
        await ctx.send("You're too annoying with your silly question!!!")
    else:
        questions.append(req)
        await ctx.send(choice(predictions))


@bot.command()
async def search(ctx, req='', num=3):
    num = int(num)
    try:
        if '://' in req:
            obj = '  or  '.join(search_by_url(req, num))
            files = os.listdir('./data')
            await ctx.send("Here are some similar images...")
            await ctx.send(f"I think you can see      {obj}        in the image")
            for i in files:
                path = 'data/' + i
                await ctx.message.channel.send(file=discord.File(path))
            for i in files:
                os.remove(f'data/{i}')
            await ctx.send(f"That's it for your request!")
        elif not req:
            await ctx.send("Why don't you try the same with url?")
            await ctx.send(">h for help")
        else:
            await ctx.send("Unfortunately, I can't find such image...")
    except Exception as e:
        await ctx.send(f"Something went wrong:( Your error is {e}")
        print('\n', e, '\n')
    except BaseException as e:
        print('\n', e, '\n')


bot.run('Njc3MDg1MTM4NzUxODQ4NDY5.XkWFTg.F3U95dyHouLUtileq8yxM_9bfBE')
