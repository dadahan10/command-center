import sys, json
from kv import call
REV = '2025-04-15'
def zero(metric):
    return {'type':'profile-metric','metric_id':metric,'measurement':'count',
            'measurement_filter':{'type':'numeric','operator':'equals','value':0},
            'timeframe_filter':{'type':'date','operator':'flow-start'},'metric_filters':None}
def notinflow(days):
    return {'type':'profile-not-in-flow','timeframe_filter':{'type':'date','operator':'in-the-last','unit':'day','quantity':days}}
def build(name, trigger, filters, steps, smart=True):
    actions, n = [], 0
    for (unit, val, tid, subj, prev, mname) in steps:
        n += 1; d = f'd{n}'; e = f'e{n}'
        if actions: actions[-1]['links']['next'] = d
        actions.append({'temporary_id':d,'type':'time-delay','data':{'unit':unit,'value':val,'secondary_value':0,'timezone':'profile'},'links':{'next':e}})
        actions.append({'temporary_id':e,'type':'send-email','links':{'next':None},'data':{'status':'draft','message':{
            'from_email':'daniel@dianarafael.com','from_label':'Diana Rafael','reply_to_email':None,'cc_email':None,'bcc_email':None,
            'subject_line':subj,'preview_text':prev,'template_id':tid,'smart_sending_enabled':smart,'transactional':False,
            'add_tracking_params':True,'custom_tracking_params':None,'additional_filters':None,'name':mname}}})
    body = {'data':{'type':'flow','attributes':{'name':name,'definition':{
        'triggers':[trigger],'profile_filter':{'condition_groups':[{'conditions':[c]} for c in filters]},
        'actions':actions,'entry_action_id':'d1'}}}}
    s, d = call('POST','flows',body,rev=REV)
    print(name, s, d['data']['id'] if s in (200,201) else str(d)[:800])
    return d

CHECKOUT = [('hours',1,'TnE3Z5','Is this the one? 💍','Your order is saved, exactly as you left it.','Checkout 1/8 Reminder'),
 ('hours',23,'YuCbnb','Can I ask what stopped you?','One tap is enough. I read every answer myself.','Checkout 2/8 What stopped you'),
 ('days',1,'XKy8hZ','Is it really a natural diamond?',"What's in your piece, and the certificate that proves it.",'Checkout 3/8 Natural diamond'),
 ('days',2,'S4kGrk','530+ reviews from people who hesitated too','Read what they wrote once the box was open.','Checkout 4/8 Reviews'),
 ('days',2,'TekMmy',"What if it doesn't fit?",'Size, returns and care, answered in one minute.','Checkout 5/8 Fit and care'),
 ('days',2,'VEnXx2','Wear it now, pay over time','Choose Affirm at checkout and see your plan before you commit.','Checkout 6/8 Affirm'),
 ('days',2,'SxSYuf','15 minutes with me?','Ask anything, see the stones on video, change what you like.','Checkout 7/8 Daniel call'),
 ('days',3,'UXVaDH','A note from me','And a gift I wanted you to know about.','Checkout 8/8 Note and gift')]
CART = [('hours',4,'UBvD9B','Still thinking about it?','Your piece is saved, exactly as you chose it.','Cart 1/8 Reminder'),
 ('hours',20,'VA7Hcx','Is it really a natural diamond?',"What's in your piece, and the certificate that proves it.",'Cart 2/8 Natural diamond'),
 ('days',2,'RPaVqY','530+ reviews from people who hesitated too','Read what they wrote once the box was open.','Cart 3/8 Reviews'),
 ('days',2,'XfE6bE','Made by hand, for you','How your piece is made, and how it gets to you.','Cart 4/8 Made to order'),
 ('days',2,'SyAYw5',"What if it doesn't fit?",'Size, returns and care, answered in one minute.','Cart 5/8 Fit and care'),
 ('days',2,'UqenfM','Wear it now, pay over time','Choose Affirm at checkout and see your plan before you commit.','Cart 6/8 Affirm'),
 ('days',2,'WAnMp5','15 minutes with me?','Ask anything, see the stones on video, change what you like.','Cart 7/8 Daniel call'),
 ('days',3,'UDhDea','A note from me','And a gift I wanted you to know about.','Cart 8/8 Note and gift')]
which = sys.argv[1]
if which == 'checkout':
    build('2026-11 | Abandoned Checkout (8)', {'type':'metric','id':'UgasKH'}, [zero('T6KBRR'), notinflow(7)], CHECKOUT)
if which == 'cart':
    build('2026-11 | Abandoned Cart (8)', {'type':'metric','id':'WT7SJV'}, [zero('UgasKH'), zero('T6KBRR'), notinflow(30)], CART)
