from marshmallow import Schema, fields

class PlainUserSchema(Schema):  
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role=fields.Str(required=True)

class UserSchema(PlainUserSchema):
    name=fields.Str(required=True)
    contact=fields.Int(required=True)
    address=fields.Str(required=True)

class UserUpdateSchema(Schema):
    name=fields.Str(required=True)
    contact=fields.Int(required=True)
    address=fields.Str(required=True)


class VehicleSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Str(required=True)
    type = fields.Str(required=True)
    owner = fields.Str(required=True)
    colour = fields.Str(required=True)
    description = fields.Str(required=True)
    is_parked=fields.Bool(dump_only=True)

class VehicleUpdateSchema(Schema):
    owner = fields.Str(required=True)
    colour = fields.Str(required=True)
    description = fields.Str(required=True)


class BuildingSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(required=True)

class FloorSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)
    building_id=fields.Int(required=True)
    

class FloorPartitionSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)
    floor_id=fields.Int(required=True)

class SlotSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)
    reserved=fields.Bool(dump_only=True)
    type=fields.Str(required=True)
    floor_partition_id=fields.Int(required=True)

class BookingSchema(Schema):
    id =  fields.Int(dump_only=True)
    slot_id=fields.Int(required=True)
    user_id=fields.Int(dump_only=True)
    park_in_time=fields.DateTime(dump_only=True)
    park_out_time=fields.DateTime()

class ShowBookingSchema(BookingSchema):
    vehicle_id =fields.Int(required=True)

class AddBookingSchema(BookingSchema):
    vehicle_number=fields.Str(required=True)



class BookingUpdateSchema(Schema):
    slot_id=fields.Int(required=True)

class BillingSchema(Schema):
    id =  fields.Int(dump_only=True)
    user_id=fields.Int(dump_only=True)
    booking_id=fields.Int(required=True)
    parking_amount=fields.Int(required=True)
