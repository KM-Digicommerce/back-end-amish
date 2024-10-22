from mongoengine import Document , fields,EmbeddedDocument

class User(Document):
    username = fields.StringField(required=True)
    email = fields.StringField(required=True)
    age = fields.IntField()

class product_type(Document):
    name = fields.StringField(required=True)
class section(Document):
    name = fields.StringField(required=True)
    product_type_list = fields.ListField(fields.ReferenceField(product_type))

class category(Document):
    name = fields.StringField(required=True)
    section_list = fields.ListField(fields.ReferenceField(section),default = [])
class Stain(Document):
    name = fields.StringField()

class products(Document):
    ManufacturerName = fields.StringField()
    tags = fields.StringField()
    product_type_id = fields.ReferenceField(product_type)
    Tags = fields.StringField()
    product_name = fields.StringField()
    Handle = fields.StringField()
    Description  = fields.StringField()
    BasePrice = fields.StringField() #price in $
    ImageURL = fields.StringField()
    Key_features = fields.StringField()
class leaf_option(EmbeddedDocument):
    leaf_count = fields.IntField()
    unfinished_price = fields.IntField()
    finished_price = fields.IntField()
    varient_code = fields.StringField()
    name = fields.StringField()

class wood_type(Document):
    name = fields.StringField()
    description = fields.StringField()
    image = fields.StringField()
    Recommended_stains = fields.ListField(fields.StringField())
   
class varient_option(Document):
    varient_count = fields.IntField()
    option_name = fields.StringField()
    option_value_id = fields.StringField()

class Variants(Document):
    product_id = fields.ReferenceField(products)
    size =  fields.StringField()
    options = fields.ReferenceField(varient_option)
    leafOptions = fields.ListField(fields.EmbeddedDocumentField(leaf_option))
    name = fields.StringField()
    Stain_id = fields.ReferenceField(Stain)
    varient_sku  =  fields.StringField()
    unfinished_price = fields.IntField()
    finished_price = fields.IntField()
    image_url =  fields.StringField()
class size_option(Document):
    name = fields.StringField()

class ignore_calls(Document):
    name = fields.StringField()
