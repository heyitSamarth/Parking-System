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
    vehicle_number = fields.Str(required=True)
    vehicle_type = fields.Str(required=True)
    vehicle_owner = fields.Str(required=True)
    vehicle_colour = fields.Str(required=True)
    vehicle_description = fields.Str(required=True)
    is_parked=fields.Bool(dump_only=True)

class VehicleUpdateSchema(Schema):
    vehicle_owner = fields.Str(required=True)
    vehicle_colour = fields.Str(required=True)
    vehicle_description = fields.Str(required=True)



# class PlainItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     price = fields.Float(required=True)


# class PlainStoreSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str()

# class PlainTagSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str()


# class ItemSchema(PlainItemSchema):
#     store_id = fields.Int(required=True, load_only=True)
#     store = fields.Nested(PlainStoreSchema(), dump_only=True)
#     tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)



# class TagSchema(PlainTagSchema):
#     store_id = fields.Int(load_only=True)
#     items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
#     store = fields.Nested(PlainStoreSchema(), dump_only=True)

# class ItemUpdateSchema(Schema):
#     name = fields.Str()
#     price = fields.Float()


# class StoreSchema(PlainStoreSchema):
#     items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
#     tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

# class TagAndItemSchema(Schema):
#     message = fields.Str()
#     item = fields.Nested(ItemSchema)
#     tag = fields.Nested(TagSchema)

