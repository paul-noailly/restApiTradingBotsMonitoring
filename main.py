from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import numpy as np
import requests

cred = credentials.Certificate("service-account-file.json")
try: 
    firebase_admin.initialize_app(cred)
    print('db initialized')
except:
    print('db already initialized')
db = firestore.client()

def dic_fix_type(dic):
    for key in dic.keys():
        value = dic[key]
        if value == 'False' or value == 'false':
            dic[key] = False
        if value == 'True' or value == 'true':
            dic[key] = True
        try:
            dic[key] = float(value)
        except:
            pass
        try:
            if int(value) == float(value):
                dic[key] = int(value)
            else:
                dic[key] = float(value)
        except:
            pass
    return dic

#initialize app
app = Flask(__name__)
api = Api(app)

CRED_ID = "11111"

# creds
class creds(Resource):
    def get(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            return db.collection(name_bot).document('creds').get().to_dict()
        else:
            return {"ERROR":""}
    def put(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            doc_ref = db.collection(name_bot).document('creds')
            new_dic = dic_fix_type(request.form.to_dict())
            doc_ref.set(new_dic,merge=False)
            return new_dic
        else:
            return {"ERROR":""},501
api.add_resource(creds, '/api&id=<cred_id>/<name_bot>/creds')

# params
class params(Resource):
    def get(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            return db.collection(name_bot).document('params').get().to_dict()
        else:
            return {"ERROR":""}
    def put(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            doc_ref = db.collection(name_bot).document('params')
            new_dic = dic_fix_type(request.form.to_dict())
            doc_ref.set(new_dic,merge=False)
            return new_dic
        else:
            return {"ERROR":""},501
api.add_resource(params, '/api&id=<cred_id>/<name_bot>/params')


# monitoring
class monitoring(Resource):
    def get(self, cred_id):
        if cred_id == CRED_ID:
            return db.collection('monitoring').document('content').get().to_dict()
        else:
            return {"ERROR":""}
    def put(self, cred_id):
        if cred_id == CRED_ID:
            doc_ref = db.collection('monitoring').document('content')
            new_dic = dic_fix_type(request.form.to_dict())
            doc_ref.set(new_dic,merge=False)
            return new_dic
        else:
            return {"ERROR":""},501
api.add_resource(monitoring, '/api&id=<cred_id>/monitoring')


# Historical trade
class htrade(Resource):
    def get(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            return db.collection(name_bot).document('htrade').get().to_dict()
        else:
            return {"ERROR":""}
    def put(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            doc_ref = db.collection(name_bot).document('htrade')
            new_dic = dic_fix_type(request.form.to_dict())
            doc_ref.set(new_dic,merge=False)
            return new_dic
        else:
            return {"ERROR":""},501
    def post(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            doc_ref = db.collection(name_bot).document('htrade')
            htrade_id = str(len(doc_ref.get().to_dict())+1)
            new_dic = {htrade_id : dic_fix_type(request.form.to_dict())}
            print('adding a new dic:\n',new_dic)
            doc_ref.set(new_dic, merge=True)
            return new_dic
        else:
            return {"ERROR":""},501
api.add_resource(htrade, '/api&id=<cred_id>/<name_bot>/htrade')

class weeklytrade(Resource):
    def get(self, cred_id, name_bot):
        if cred_id == CRED_ID:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=7)
            htrade_dic = db.collection(name_bot).document('htrade').get().to_dict()
            bot_message = 'Weekly performances: (from {} to {})\n'.format(start_date.strftime(format='%Y-%m-%d'),end_date.strftime(format='%Y-%m-%d'))
            start_date, end_date = start_date.strftime(format='%Y-%m-%d %H:%M:%S:%f'), end_date.strftime(format='%Y-%m-%d %H:%M:%S:%f')
            list_return = []
            list_size = []
            nbs_long = 0
            nbs_acc = 0
            for key in htrade_dic.keys():
                trade_dict = htrade_dic[key]
                if trade_dict['date_exit'] > start_date and trade_dict['date_exit'] < end_date:
                    list_return.append(trade_dict['return'])
                    list_size.append(trade_dict['size'])
                    if trade_dict['direction'] == 1:
                        nbs_long += 1
                    if trade_dict['return'] > 0:
                        nbs_acc += 1
            list_return, list_size = np.array(list_return), np.array(list_size)
            avg_return = list_return.mean()
            total_return = list_return.sum()
            if len(list_return) != 0:
                accuracy = nbs_acc/len(list_return)
                prop_long = nbs_long/len(list_return)
                nbs_trade = len(list_return)
                bot_message += '- Total return: {:.4%} \n- Avg return: {:.4%} \n- Accuracy: {:.2%} \n- % of longs: {:.2%} \n- Number of trades: {}'.format(total_return, avg_return, accuracy, prop_long, nbs_trade)
            else:

                bot_message += 'No trades have been made.'
            creds = db.collection(name_bot).document('creds').get().to_dict()
            telegram_token, telegram_chat_id = creds['telegram_token'] , creds['telegram_chat_id'] 
            send_text = 'https://api.telegram.org/bot' + str(telegram_token) + '/sendMessage?chat_id=' + str(telegram_chat_id) + '&parse_mode=Markdown&text=' + bot_message
            response = requests.get(send_text)
            return {"status":"message have been succefully sent."}
        else:
            return {"ERROR":""}
api.add_resource(weeklytrade, '/api&id=<cred_id>/<name_bot>/weeklytrade')
