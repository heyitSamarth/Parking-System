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

class UserDetailSchema(Schema):
    name=fields.Str(required=True)
    role=fields.Str(required=True)
    username = fields.Str(required=True)


class UserUpdateSchema(Schema):
    name=fields.Str(required=True)
    contact=fields.Int(required=True)
    address=fields.Str(required=True)

class BookingSchema(Schema):
    id =  fields.Int(dump_only=True)
    slot_id=fields.Int(required=True)
    user_id=fields.Int(dump_only=True)
    park_in_time=fields.DateTime(dump_only=True)
    park_out_time=fields.DateTime()

class PlainVehicleSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Str(required=True)
    type = fields.Str(required=True)
    owner = fields.Str(required=True)
    colour = fields.Str(required=True)
    description = fields.Str(required=True)
    is_parked=fields.Bool(dump_only=True)

class VehicleSchema(PlainVehicleSchema):
    bookings=fields.List(fields.Nested(BookingSchema), dump_only=True)

class VehicleUpdateSchema(Schema):
    owner = fields.Str(required=True)
    colour = fields.Str(required=True)
    description = fields.Str(required=True)

class PlainBuildingSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(required=True)
class PlainFloorSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)

class PlainFloorPartitionSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)

class PlainSlotSchema(Schema):
    id =  fields.Int(dump_only=True)
    number =fields.Int(dump_only=True)
    reserved=fields.Bool(dump_only=True)
    type=fields.Str(required=True)

class BuildingSchema(PlainBuildingSchema):
    floors = fields.List(fields.Nested(PlainFloorSchema), dump_only=True)

class FloorSchema(PlainFloorSchema):
    building_id=fields.Int(required=True)
    building = fields.Nested(PlainBuildingSchema(), dump_only=True)
    floor_partitions=fields.List(fields.Nested(PlainFloorPartitionSchema), dump_only=True)

class FloorPartitionSchema(PlainFloorPartitionSchema):
    floor_id=fields.Int(required=True)
    floor= fields.Nested(PlainFloorSchema(), dump_only=True)
    slots=fields.List(fields.Nested(PlainSlotSchema), dump_only=True)

class SlotSchema(PlainSlotSchema):
    floor_partition_id=fields.Int(required=True)
    floor_partition=fields.Nested(PlainFloorPartitionSchema(), dump_only=True)
    bookings=fields.List(fields.Nested(BookingSchema), dump_only=True)

class PlainBillingSchema(Schema):
    id =  fields.Int(dump_only=True)
    user_id=fields.Int(dump_only=True)
    booking_id=fields.Int(required=True)
    parking_amount=fields.Int(required=True)


class ShowBookingSchema(BookingSchema):
    vehicle_id =fields.Int(required=True)
    vehicle=fields.Nested(PlainVehicleSchema(), dump_only=True)
    slot=fields.Nested(PlainSlotSchema(), dump_only=True)
    user=fields.Nested(UserDetailSchema(), dump_only=True)
    billing=fields.List(fields.Nested(PlainBillingSchema), dump_only=True)

class BillingSchema(PlainBillingSchema):
    booking=fields.Nested(BookingSchema(), dump_only=True)







class AddBookingSchema(BookingSchema):
    vehicle_number=fields.Str(required=True)



class BookingUpdateSchema(Schema):
    slot_id=fields.Int(required=True)


