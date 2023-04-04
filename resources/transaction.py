from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import TransactionSchema
from models import TransactionModel,BillingModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("transactions","Transactions",__name__,description="Operations on Transactions")


@blp.route("/transaction")
class Transactition(MethodView):
    @jwt_required()
    @blp.arguments(TransactionSchema)
    def post(Self,transaction_data):
        billing = BillingModel.query.filter(BillingModel.id==transaction_data["billing_id"]).first()
        if billing:
            previous_transactions=TransactionModel.query.filter(BillingModel.id==transaction_data["billing_id"]).first()
            if previous_transactions:
                previous_transaction=TransactionModel.query.filter(BillingModel.id==transaction_data["billing_id"]).order_by(TransactionModel.id.desc()).first()
                amount_pending=previous_transaction.amount_pending-transaction_data["amount"]
                if(previous_transaction.amount_pending==0):
                    abort(409,message="total amount has been paid ")
                if(previous_transaction.amount_pending<transaction_data["amount"]):
                    abort(409,message="Plz enter correct amount  ")
                    
            else:
                if(billing.parking_amount<transaction_data["amount"]):
                    abort(409,message="Plz enter correct amount  ")
                amount_pending=billing.parking_amount-transaction_data["amount"]

            transaction=TransactionModel(
                billing_id=transaction_data["billing_id"],
                amount=transaction_data["amount"],
                amount_pending=amount_pending,
                payment_type=transaction_data["payment_type"]
            )
            db.session.add(transaction)
            db.session.commit()
            return {"message":"transactition created Succesfully"},201
        else:
            abort(400,message="Plz enter correct billing id")
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        transactitions = TransactionModel.query.all()
        return transactitions


@blp.route("/transaction/<transaction_id>")
class TransactitionOperation(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        transactition = TransactionModel.query.filter(TransactionModel.id==transaction_id).first()
        if transactition :
            return transactition
        else :
            abort(400,message="Plz enter correct transaction id")
    
    @jwt_required()
    def delete(self, transaction_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        transaction = TransactionModel.query.filter(TransactionModel.id==transaction_id).first()
        if transaction :
            db.session.delete(transaction)
            db.session.commit()
            return {"message": "transactition deleted."}, 204
        else :
            abort(400,message="Plz enter correct transactition id")

    # <- Update Transactition ->
    # @jwt_required()
    # @blp.arguments(TransactitionUpdateSchema)
    # @blp.response(201,TransactitionSchema)
    # def put(self,transactition_data,transactition_id):
    #     jwt=get_jwt()
    #     if not jwt.get("is_admin"):
    #         abort(401,message="admin privilege required ")
    #     transactition = TransactitionModel.query.filter(TransactitionModel.id==transactition_id).first()
    #     if transactition:
    #         transactition.slot_id=transactition_data["slot_id"]
    #     else:
    #         abort(401,message="Enter correct transactition id")
    #     db.session.add(transactition)
    #     db.session.commit()
    #     return transactition
        