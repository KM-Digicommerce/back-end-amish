from mongoengine import Document , fields,EmbeddedDocument
from datetime import datetime
class user(Document):
    name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    role = fields.StringField()
    password = fields.StringField()

class brand(Document):
    name = fields.StringField()

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

class type_name(Document):
    name = fields.StringField()

class type_value(Document):
    name = fields.StringField()
    images = fields.ListField(fields.StringField())

class varient_option(Document):
    option_name_id = fields.ReferenceField(type_name)
    option_value_id_list = fields.ListField(fields.ReferenceField(type_value),default = [])

class product_varient_option(Document):
    option_name_id = fields.ReferenceField(type_name)
    option_value_id = fields.ReferenceField(type_value)

class product_varient(Document):
    sku_number = fields.StringField(required=True)
    varient_option_id = fields.ListField(fields.ReferenceField(product_varient_option))
    image_url = fields.ListField(fields.StringField())
    finished_price = fields.StringField()
    un_finished_price = fields.StringField()
    quantity = fields.StringField()

class products(Document):
    model = fields.StringField()
    mpn = fields.StringField()
    upc_ean = fields.StringField(default = "")
    breadcrumb = fields.StringField()
    brand_id = fields.ReferenceField(brand)
    product_name = fields.StringField()
    long_description = fields.StringField()
    short_description = fields.StringField()
    features = fields.StringField()
    attributes = fields.StringField()
    tags = fields.StringField()
    msrp = fields.StringField()
    base_price = fields.StringField()
    key_features = fields.StringField()
    options = fields.ListField(fields.ReferenceField(product_varient))
    image = fields.ListField(fields.StringField())

class leaf_option(EmbeddedDocument):
    leaf_count = fields.IntField()
    unfinished_price = fields.StringField()
    finished_price = fields.StringField()
    varient_code = fields.StringField()
    name = fields.StringField()

class ignore_calls(Document):
    name = fields.StringField()

class product_category_config(Document):
    product_id = fields.ReferenceField(products)
    category_level = fields.StringField()
    category_id = fields.StringField()

class vendor(Document):
    name = fields.StringField(required=True)
    manufacture = fields.StringField()

class category_varient(Document):
    category_id = fields.StringField()
    varient_option_id_list = fields.ListField(fields.ReferenceField(varient_option),default = [])

class capability(Document):
    action_name = fields.StringField()
    role_list = fields.ListField(fields.StringField(),default = [])


class email_otp(Document):
    email = fields.EmailField(unique=True)
    otp = fields.StringField()
    expires_at = fields.DateTimeField()

    def __str__(self):
        return f'OTP for {self.email}'
    
class category_log(Document):
    category_id = fields.StringField()
    action = fields.StringField() 
    log_date = fields.DateTimeField(default=datetime.now)
    user_id = fields.ReferenceField(user)
    level = fields.StringField()
    
class product_log(Document):
    product_id = fields.ReferenceField(products)
    action = fields.StringField()
    log_date = fields.DateTimeField(default=datetime.now)
    user_id = fields.ReferenceField(user)
    
class product_varient_log(Document):
    product_varient_id = fields.ReferenceField(product_varient)
    action = fields.StringField()
    log_date = fields.DateTimeField(default=datetime.now)
    user_id = fields.ReferenceField(user)
class category_varient_option_log(Document):
    category_id = fields.StringField()
    level = fields.StringField()
    category_varient_option_id = fields.ReferenceField(varient_option)
    action = fields.StringField()
    log_date = fields.DateTimeField(default=datetime.now)
    user_id = fields.ReferenceField(user)

class price_log(Document):
    name = fields.StringField()
    product_id = fields.ReferenceField(products)
    product_varient_id = fields.ReferenceField(product_varient)
    user_id = fields.ReferenceField(user)
    log_date = fields.DateTimeField(default=datetime.now)
    
    
    