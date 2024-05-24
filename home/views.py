
from django.shortcuts import render, redirect
from . models import *
from register.models import Static
from django.contrib import messages
import random
from django.contrib.auth import logout 
from operator import itemgetter
import psycopg2
from django.db.models import Sum
from django.http import JsonResponse
from nudenet import NudeDetector
from PIL import Image


def logout_user(request):
    logout(request)
    messages.info(request, 'Your were logged out')
    return redirect('lgn')


def suggestion(request):
    x = Static.objects.all()
    cats = Category.objects.all()

    if request.method == 'POST':

        cat = request.POST['cat']
        reg = request.POST['reg']
        ide = request.POST['ide']
        msg = request.POST['msg']
        no_like = 0
        no_comment = 0
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        audio = request.FILES.get('audio')
        nickname = request.POST['nickname']
        code = random.randint(0, 9999)
        msg2 = Messages.objects.filter(pkv=code)
        words2 = [
                "BUTTOCKS_EXPOSED",
                "FEMALE_BREAST_EXPOSED",
                "FEMALE_GENITALIA_EXPOSED",
                "MALE_BREAST_EXPOSED",
                "ANUS_EXPOSED",
                "FEET_EXPOSED",
                "BELLY_EXPOSED",
                "MALE_GENITALIA_EXPOSED"
            ]
        porn  = []
        
        words = ['liberal', 'conservative', 'socialist', 'communist', 'facist', 'democrat', 'republican', 
                 'liberation', 'green', 'anarchist', 'democracy', 'monarchy', 'oligarchy', 'theocracy', 'republic',
                 'federalism', 'confederation', 'authoritarianism', 'totalitarianism', 'freedom', 'justice', 'equality',
                 'rights', 'power', 'corruption', 'imperialism', 'nationalism', 'globalization', 'populism',
                 'sex', 'penis', 'vigina', 'pussy', 'milf', 'cock', 'anus', 'fuck', 'fucking', 'fucked', 'blowjob'
                 ]
        
        if len(cat) == 0 or len(msg) == 0:
            messages.info(request, 'Fields cannot be empty...' ) 
            return render(request, 'messages.html')
        
        elif any(word in msg.lower() for word in words):
            messages.info(request, 'Your message is not valid to be sent...' ) 
            return render(request, 'messages.html')
        else:
            
            new_message = Messages(pkv=code,
                                cat=cat,
                                reg=reg,
                                identity=ide,
                                msg=msg,
                                no_likes=no_like,
                                no_comments=no_comment,
                                nickname=nickname,
                                image=image,
                                image2=image,
                                video=video,
                                audio=audio)
            new_message.save()
            for xxx in msg2:
                if xxx.image:
                    xx = xxx.image.path
                    detector = NudeDetector()
                    data = detector.detect(xx[0:])
                    for item in data:
                        for key in item.items():
                            if any(word in key for word in words2):
                                porn.append(key)
            if len(porn) > 0:
                delete_msg = Messages.objects.filter(pkv=code)
                delete_msg.delete()
                messages.info(request, 'You cannot send this message, due to adult content attached to it !')
                return render(request, 'messages.html')
            else:
                messages.info(request, 'Your suggestion has been sent successfully')
                return render(request, 'messages.html')
    else:
        return render(request, 'suggestion.html', {'x': x,
                                                   'cats': cats})
    
def inbox(request):

    x = Static.objects.all()
    icons = Icon.objects.all()
    msgs = Messages.objects.all()
    replys = Replys.objects.all()
    comments = Comments.objects.all()
    likes = Likes.objects.all()
    like_inbox = request.session.get('likes')
    number_of_likes = None
    for msg in msgs:
        for like in likes:
            if msg.pkv == like.pkv:
                num_of_likes = int(like.pkv)
                number_of_likes = int(Likes.objects.filter(pkv=num_of_likes).count())
        
    return render(request, 'inbox.html', {'x': x,
                                          'icons': icons,
                                          'msgs': msgs,
                                          'replys': replys,
                                          'comments': comments,
                                          'likes': number_of_likes})

def inbox_admin(request):

    x = Static.objects.all()
    msgs = Messages.objects.all()
    replys = Replys.objects.all()
    comments = Comments.objects.all()
    icons = Icon.objects.all()
    

    return render(request, 'inbox_admin.html', {'x': x,
                                          'msgs': msgs,
                                          'replys': replys,
                                          'comments': comments,
                                          'icons': icons})

def view_message(request, pk):

    x = Static.objects.all()
    usericon = UserIcon.objects.all()
    msgs = Messages.objects.get(pk=pk)
    msgs2 = Messages.objects.all()
    icons = Icon.objects.all()
    replys = Replys.objects.all()
    comments = Comments.objects.filter(pkv=pk)
    number = int(Comments.objects.filter(pkv=pk).count())
    likes = int(Likes.objects.filter(pkv=pk).count())
    request.session['likes'] = likes

    words = [
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "FEET_EXPOSED",
    "BELLY_EXPOSED",
    "MALE_GENITALIA_EXPOSED"
]
    porn  = []
    for xxx in msgs2.filter(pk=pk):
        if xxx.image:
            xx = xxx.image.path
            detector = NudeDetector()
            data = detector.detect(xx[0:])
            for item in data:
                for key in item.items():
                    if any(word in key for word in words):
                        porn.append(key)
    if len(porn) > 0:
        messages.info(request, 'This message cannot be viewed due to Adult Content posted by this student !')
        return render(request, 'messages.html')

    if request.method == 'POST':


        pkv = request.POST.get('pkv')
        reg = request.POST.get('reg')
        replied = request.POST.get('replied')
        no_comment = request.POST.get('no_comment')
        msg_replied = request.POST.get('msg_replied')
        comment = request.POST.get('comment')
        nickname1 = request.POST.get('nickname1')
        nickname2 = request.POST.get('nickname2')
    
        
        new_comment = Comments.objects.create(pkv=pkv)
        new_comment.reg = reg
        new_comment.replied = replied
        new_comment.msg_replied = msg_replied
        new_comment.msg = comment
        new_comment.username = nickname1
        new_comment.nickname = nickname2
        new_comment.save()
        new_comment2 = Messages.objects.get(pkv=pkv)
        new_comment2.no_comments = no_comment
        new_comment2.save()
        return redirect('/home/view_message/'+pk)
        #delete_comment = Comments.objects.filter(reg=reg)
    return render(request, 'view_message.html', {'x': x,
                                          'msgs': msgs,
                                            'replys': replys,
                                           'comments': comments,
                                          'icons': icons,
                                          #'deletes': delete_comment,
                                          'number': number,
                                          'likes': likes,
                                          'usericon': usericon})

def like(request):

    likes = Likes.objects.all()

    if request.method == 'POST':

        pkv = request.POST.get('pkv2')
        reg = request.POST.get('reg2')
        replied = request.POST.get('replied2')
        nickname1 = request.POST.get('nickname12')
        like = request.POST.get('like')
        no_like = request.POST.get('no_like')


        if Likes.objects.filter(pkv=pkv, reg=reg).exists():

            delete_like = Likes.objects.get(pkv=pkv, reg=reg)
            delete_like.delete()
            return redirect('view_message/'+ pkv)
        else:
            new_like = Messages.objects.get(pkv=pkv)
            new_like.no_likes = no_like
            new_like.save()
            new_comment = Likes.objects.create(pkv=pkv)
            new_comment.reg = reg
            new_comment.replied = replied
            new_comment.username = nickname1
            new_comment.like = like
            new_comment.save()
            return redirect('view_message/'+ pkv)

    return render(request, 'view_message.html', {})

def reply(request, pk):

    x = Static.objects.all()
    usericon = UserIcon.objects.all()
    msgs = Messages.objects.get(pk=pk)
    icons = Icon.objects.all()
    replys = Replys.objects.all()
    comments = Comments.objects.filter(pkv=pk)
    number = int(Comments.objects.filter(pkv=pk).count())
    likes = int(Likes.objects.filter(pkv=pk).count())

    if request.method == 'POST':

        pkv  = request.POST['pkv']
        reply = request.POST['reply']
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        audio = request.FILES.get('audio')

        if Replys.objects.filter(pkv=pkv).exists():
            if image:
                new_del = Replys.objects.get(pkv=pkv)
                new_del.image.delete()
                new_edit = Replys.objects.get(pkv=pkv)
                new_edit.reply = reply
                new_edit.image = image
                new_edit.save()
                return redirect('/home/reply/'+pkv) 
            elif audio:
                new_del = Replys.objects.get(pkv=pkv)
                new_del.audio.delete()
                new_edit = Replys.objects.get(pkv=pkv)
                new_edit.reply = reply
                new_edit.audio = audio
                new_edit.save()
                return redirect('/home/reply/'+pkv)
            elif video:
                new_del = Replys.objects.get(pkv=pkv)
                new_del.video.delete()
                new_edit = Replys.objects.get(pkv=pkv)
                new_edit.reply = reply
                new_edit.video = video
                new_edit.save()
                return redirect('/home/reply/'+pkv)
            else:
                new_edit = Replys.objects.get(pkv=pkv)
                new_edit.reply = reply
                new_edit.save()
                
        else:
            new_admin_reply = Replys(pkv=pkv,
                                    reply=reply,
                                    image=image,
                                    audio=audio,
                                    video=video)
            new_admin_reply.save()
        return redirect('/home/reply/'+pkv)
    return render(request, 'reply.html', {'x': x,
                                          'msgs': msgs,
                                            'replys': replys,
                                           'comments': comments,
                                          'icons': icons,
                                          'likes': likes,
                                          'number': number,
                                          'usericon': usericon})

def inprivate(request):

    x = Static.objects.all()

    if request.method == 'POST':

        cat = request.POST['cat']
        reg = request.POST['reg']
        ide = request.POST['ide']
        msg = request.POST['msg']
        nickname = request.POST['nickname']
        like = str(0)
        code = random.randint(0, 9999)
        words = ['liberal', 'conservative', 'socialist', 'communist', 'facist', 'democrat', 'republican', 
                 'liberation', 'green', 'anarchist', 'democracy', 'monarchy', 'oligarchy', 'theocracy', 'republic',
                 'federalism', 'confederation', 'authoritarianism', 'totalitarianism', 'freedom', 'justice', 'equality',
                 'rights', 'power', 'corruption', 'imperialism', 'nationalism', 'globalization', 'populism',
                 'sex', 'penis', 'vigina', 'pussy', 'milf', 'cock', 'anus', 'fuck', 'fucking', 'fucked', 'blowjob'
                 ]
        if any(word in msg.lower() for word in words):
            messages.info(request, 'Your anonymous message is not valid to be sent...' ) 
            return render(request, 'messages.html')
        else:
            new_message = Messages(pkv=code,
                                cat=cat,
                                reg=reg,
                                identity=ide,
                                msg=msg,
                                nickname=nickname)
            new_message.save()
            messages.info(request, 'Your anonymous suggestion has been sent successfully')
            return render(request, 'messages.html')
    else:
        return render(request, 'inprivate.html', {'x': x})
    
def outbox(request):
    x = Static.objects.all()
    msgs = Messages.objects.all().order_by('timestamp')
    msgs2 = Messages.objects.all()
    replys = Replys.objects.all()
    icons = Icon.objects.all()

    return render(request, 'outbox.html', {'x': x,
                                           'replys': replys,
                                           'msgs': msgs,
                                           'msgs2': msgs2,
                                           'icons': icons})

def edit(request, pk):
    msgs = Messages.objects.get(pk=pk)
    msgs2 = Messages.objects.filter(pk=pk)
    icons = Icon.objects.all()

    if request.method == 'POST':

        pkv  = request.POST.get('pkv')
        cat  = request.POST['cat']
        reg = request.POST['reg']
        identity  = request.POST['identity']
        edit = request.POST['edit']
        img = request.FILES.get('image')
        video = request.FILES.get('video')
        audio = request.FILES.get('audio')
        msg2 = Messages.objects.filter(pkv=pkv)

        words2 = [
                "BUTTOCKS_EXPOSED",
                "FEMALE_BREAST_EXPOSED",
                "FEMALE_GENITALIA_EXPOSED",
                "MALE_BREAST_EXPOSED",
                "ANUS_EXPOSED",
                "FEET_EXPOSED",
                "BELLY_EXPOSED",
                "MALE_GENITALIA_EXPOSED"
            ]
        
        
        words = ['liberal', 'conservative', 'socialist', 'communist', 'facist', 'democrat', 'republican', 
                 'liberation', 'green', 'anarchist', 'democracy', 'monarchy', 'oligarchy', 'theocracy', 'republic',
                 'federalism', 'confederation', 'authoritarianism', 'totalitarianism', 'freedom', 'justice', 'equality',
                 'rights', 'power', 'corruption', 'imperialism', 'nationalism', 'globalization', 'populism',
                 'sex', 'penis', 'vigina', 'pussy', 'milf', 'cock', 'anus', 'fuck', 'fucking', 'fucked', 'blowjob'
                 ]

        if len(cat) == 0 or len(edit) == 0:
            messages.info(request, 'Fields cannot be empty...' ) 
            return render(request, 'messages.html')
        
        elif any(word in edit.lower() for word in words):
            messages.info(request, 'Your message is not valid to be sent...' ) 
            return render(request, 'messages.html')
        else:
            if audio:
                new_del = Messages.objects.get(pkv=pkv)
                new_del.audio.delete()
                new_edit = Messages.objects.get(pkv=pkv)
                new_edit.msg = edit
                new_edit.audio = audio
                new_edit.save()
                return redirect('/home/edit/'+pkv)
            elif video:
                new_del = Messages.objects.get(pkv=pkv)
                new_del.video.delete()
                new_edit = Messages.objects.get(pkv=pkv)
                new_edit.msg = edit
                new_edit.video = video
                new_edit.save()
                return redirect('/home/edit/'+pkv)
            elif img:
                porn  = []
                f1_edit = Messages.objects.get(pkv=pkv)
                f1_edit.msg = edit
                f1_edit.image = img
                f1_edit.save()
                for xxx in msg2:
                    if xxx.image:
                        xx = xxx.image.path
                        detector = NudeDetector()
                        data = detector.detect(xx[0:])
                        for item in data:
                            for key in item.items():
                                if any(word in key for word in words2):
                                    porn.append(key)
                if len(porn) > 0:
                    
                    delete_pic = Messages.objects.get(pkv=pkv)
                    delete_pic.image.delete()
                    save_pic = Messages.objects.get(pkv=pkv)
                    saved_pic = Messages.objects.get(pkv=pkv)
                    saved_pic.image = save_pic.image2
                    saved_pic.save()
                    return redirect('/home/edit/'+pkv)
                else:
                    new_del = Messages.objects.get(pkv=pkv)
                    new_del.image.delete()
                    new_edit = Messages.objects.get(pkv=pkv)
                    new_edit.msg = edit
                    new_edit.image = img
                    new_edit.image2 = img
                    new_edit.save()
                    return redirect('/home/edit/'+pkv)
            else:
                None
            new_edit = Messages.objects.get(pkv=pkv)
            new_edit.msg = edit
            new_edit.save() 
            return redirect('/home/edit/'+pkv)
    return render(request, 'edit.html', {'msgs': msgs,
                                         'icons': icons})

def delete_outbox(request, pk):

    dl_outbox = Messages.objects.get(pk=pk)
    dl_outbox.delete()

    return redirect('outbox')

"""def delete_image(request, pk):

    dl_outbox = Messages.objects.get(pk=pk)
    dl_outbox.image.delete()
    dl_outbox.image2.delete()

    return redirect('outbox')

def delete_audio(request, pk):

    dl_outbox = Messages.objects.get(pk=pk)
    dl_outbox.audio.delete()

    return redirect('/home/edit/'+pk)

def delete_video(request, pk):

    dl_outbox = Messages.objects.get(pk=pk)
    dl_outbox.video.delete()

    return redirect('/home/edit/'+pk)"""


def mycomments(request):

    x = Static.objects.all()
    mycomment = Comments.objects.all()
    replied_message = Messages.objects.all()

    return render(request, 'mycomments.html', {'mycomment': mycomment,
                                               'replied': replied_message,
                                               'x': x})

def delete_comment(request, pk):

    dl_comment = Comments.objects.get(pk=pk)
    dl_comment.delete()
    return redirect('mycomments')

def analysis(request):

    code = Messages.objects.all()

    """var_a = psycopg2.connect(database ='ossb2',
                            user ='postgres',
                            password = '3814',
                            host = 'localhost',
                            port = '5432')
    
    cursor_var_a= var_a.cursor()

    command_var_a = 'select cat from home_Messages'
    cursor_var_a.execute(command_var_a)"""

    cursor_var_a = Messages.objects.values('cat')

    list_var_a = []

    words = ['DACS', 'Library', 'Personal', 'Fees', 'faculty',
             'Other', 'Sports', 'Medicals', 'Hostel']

    for item in cursor_var_a:
        for key in item.items():
            if any(word in key for word in words):
                list_var_a.append(key[1])

    print(list_var_a)    
    
    uniq = []
    for str in list_var_a:
        if str not in uniq:
            uniq.append(str)
    print(uniq)

    it = []
    var = 'x'

    for itt in list_var_a:
        if itt != var:
            var = itt
            it.append(int(Messages.objects.filter(cat=itt).count()))

    print(it)

    context = {
        'code': code,
        'uni_list': uniq,
        'rate': it,
    }
    return render(request, 'analysis.html', context)