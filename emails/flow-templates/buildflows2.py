import sys
from kv import call
from buildflows import zero, notinflow
REV = '2025-04-15'
def build(name, trigger, filters, steps, smart=True):
    actions = []
    def add(a):
        if actions: actions[-1]['links']['next'] = a['temporary_id']
        actions.append(a)
    for n, st in enumerate(steps, 1):
        unit, val, tid, subj, prev, mname = st[:6]
        extra = st[6] if len(st) > 6 else None
        if unit:
            add({'temporary_id':f'd{n}','type':'time-delay','data':{'unit':unit,'value':val,'secondary_value':0,'timezone':'profile'},'links':{'next':None}})
        add({'temporary_id':f'e{n}','type':'send-email','links':{'next':None},'data':{'status':'draft','message':{
            'from_email':'daniel@dianarafael.com','from_label':'Diana Rafael','reply_to_email':None,'cc_email':None,'bcc_email':None,
            'subject_line':subj,'preview_text':prev,'template_id':tid,'smart_sending_enabled':smart,'transactional':False,
            'add_tracking_params':True,'custom_tracking_params':None,
            'additional_filters':({'condition_groups':[{'conditions':[c]} for c in extra]} if extra else None),'name':mname}}})
    body = {'data':{'type':'flow','attributes':{'name':name,'definition':{
        'triggers':[trigger],'profile_filter':({'condition_groups':[{'conditions':[c]} for c in filters]} if filters else None),
        'actions':actions,'entry_action_id':actions[0]['temporary_id']}}}}
    s, d = call('POST','flows',body,rev=REV)
    print(name, s, d['data']['id'] if s in (200,201) else str(d)[:900])
M = lambda i: {'type':'metric','id':i}
w = sys.argv[1]
if w == 'post':
    build('2026-11 | Post-purchase: order confirmed + studio', M('T6KBRR'), None, [
        (None,0,'Wz5xiT',"Your order is confirmed. Here's what happens now.",'Made by hand in our studio, checked, and shipped insured within 10 business days.','PP 1/4 Order confirmed'),
        ('days',5,'R7aCs4','Inside the studio while your piece is made','A look at the bench: setting, polishing and the final check.','PP 2/4 Inside the studio',[zero('Yu3gpi')])], smart=False)
if w == 'shipped':
    build('2026-11 | Post-purchase: shipped + tracking + customs', M('Yu3gpi'), None, [
        (None,0,'VWquHb','Your piece has shipped. Tracking inside.','Your tracking number, a short note on customs, and how to care for your piece.','PP 3/4 Shipped')], smart=False)
if w == 'delivered':
    build('2026-11 | Delivered: Google review + cross-sell (60d)', M('Uin4Gb'), None, [
        ('days',3,'VM9Y2p','How does it feel to wear it?',"One minute on Google helps the next person trust a studio they've never met.",'PP 4/4 Google review'),
        ('days',57,'SnRXLp','Made to go with yours',"A few pieces we'd pair with what you're already wearing.",'CrossSell 1/3 Made to go with yours'),
        ('days',4,'U4qkKw','How our customers wear theirs','Same gold, same diamonds, worn together.','CrossSell 2/3 Worn together'),
        ('days',5,'YsXbez','Want it designed to match? 15 minutes with Daniel','We can make the second piece to fit the first exactly.','CrossSell 3/3 Designed to match')], smart=False)
if w == 'browse':
    build('2026-11 | Browse abandonment (4)', M('RdGtZY'), [zero('T6KBRR'), zero('UgasKH'), zero('WT7SJV'), notinflow(14)], [
        ('hours',2,'TQqPSp','Still thinking about the {{ event.Name }}?','Made to order for you, shipped insured on us, with lifetime care.','Browse 1/4 The piece you viewed'),
        ('hours',22,'UibmNe',"Why 530+ customers trusted a studio they'd never visited",'Natural diamonds, solid gold, made by hand since 2014.','Browse 2/4 Why us'),
        ('days',2,'XbnPRb','A gift with the {{ event.Name }}: 1 ct studs','Free 1 ct natural black diamond studs, now from $2,000 (was $3,000).','Browse 3/4 Studs gift'),
        ('days',2,'SNfvwN','Questions about the {{ event.Name }}? 15 minutes with Daniel','Size, gold, stone, budget: ask a person, not a chatbot.','Browse 4/4 Daniel call')])
if w == 'jv':
    build('2026-11 | JEWELVERSARY (order +365d)', M('T6KBRR'), None, [
        ('days',365,'Tg23sD',"Happy JEWELVERSARY, {{ first_name|default:'friend' }}",'One year ago today, you chose a piece from our studio.','JEWELVERSARY')], smart=False)
