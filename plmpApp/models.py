from mongoengine import Document , fields,EmbeddedDocument

class User(Document):
    user_name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    age = fields.IntField()

class product_type(Document):
    name = fields.StringField(required=True)
class section(Document):
    name = fields.StringField(required=True)
    product_type_list = fields.ListField(fields.ReferenceField(product_type))

class level_five_category(Document):
    name = fields.StringField(required=True)

class level_four_category(Document):
    name = fields.StringField(required=True)
    level_five_category_list = fields.ListField(fields.ReferenceField(level_five_category),default = [])

class level_three_category(Document):
    name = fields.StringField(required=True)
    level_four_category_list = fields.ListField(fields.ReferenceField(level_four_category),default = [])

class level_two_category(Document):
    name = fields.StringField(required=True)
    level_three_category_list = fields.ListField(fields.ReferenceField(level_three_category),default = [])

class level_one_category(Document):
    name = fields.StringField(required=True)
    level_two_category_list = fields.ListField(fields.ReferenceField(level_two_category),default = [])

class category(Document):
    name = fields.StringField(required=True)
    level_one_category_list = fields.ListField(fields.ReferenceField(level_one_category),default = [])
    
class Stain(Document):
    name = fields.StringField()

class products(Document):
    Manufacturer_name = fields.StringField()
    tags = fields.StringField()
    category_level_id = fields.StringField()
    Tags = fields.StringField()
    product_name = fields.StringField()
    Handle = fields.StringField()
    Description  = fields.StringField()
    BasePrice = fields.StringField() #price in $
    ImageURL = fields.ListField()
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
    options = fields.ListField(fields.ReferenceField(varient_option))
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

class category_level(Document):
    name = fields.StringField()
class product_category_config(Document):
    product_id = fields.ReferenceField(products)
    category_level = fields.ReferenceField(category_level)
    category_id = fields.StringField()
