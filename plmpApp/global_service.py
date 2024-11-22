import redis
import pickle

class DatabaseModel:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=False)
    @staticmethod
    def get_document(queryset, filter={}, field_list=[]):
        try:
            # Create a cache key with the collection name and filter
            cache_key = f"{queryset}:get_document:{str(filter)}"
            cached_data = DatabaseModel.redis_client.get(cache_key)
            if cached_data:
                print(pickle.loads(cached_data))
                return pickle.loads(cached_data)
            
            # Fetch data from the database
            data = queryset.filter(**filter).only(*field_list).limit(1)
            
            if data:
                data = data[0]
                # Cache the data
                DatabaseModel.redis_client.setex(cache_key, 3600, pickle.dumps(data))
                return data
            else:
                return None
        except Exception as e:
            print(f"Error occurred while fetching document: {e}")
            return None

    @staticmethod
    def list_documents(queryset, filter={}, field_list=[], sort_list=[], lower_limit=None, upper_limit=None):
        try:
            # Create a cache key with collection name, filter, and sort options
            cache_key = f"{queryset}:list_documents:{str(filter)}:{str(sort_list)}:{lower_limit}-{upper_limit}"
            cached_data = DatabaseModel.redis_client.get(cache_key)
            
            if cached_data:
                return pickle.loads(cached_data)
            
            # Fetch data from the database
            data = queryset(**filter).skip(lower_limit).limit(upper_limit - lower_limit if lower_limit is not None and upper_limit is not None else None).only(*field_list).order_by(*sort_list)
            
            if data:
                # Cache the data
                DatabaseModel.redis_client.setex(cache_key, 3600, pickle.dumps(data))
                return data
            else:
                return []  
        except Exception as e:
            print(f"Error occurred while fetching documents: {e}")
            return []

    @staticmethod
    def update_documents(queryset, filter={}, json={}):
        try:
            # Perform the update operation
            data = queryset.filter(**filter).update(**json)
            
            if data:
                # After updating, invalidate the cache for the specific collection
                pattern = f"{queryset}:*"  # Match all keys for the collection
                keys = DatabaseModel.redis_client.keys(pattern)
                if keys:
                    DatabaseModel.redis_client.delete(*keys)
            
            return bool(data)
        except Exception as e:
            print(f"Error occurred while updating documents: {e}")
            return False
    
    def save_documents(queryset,  json={}):
        obj = queryset(**json)
        obj.save()
        return obj

    def delete_documents(queryset,  json={}):
        queryset(**json).delete()
        return True
    def count_documents(queryset,filter={}):
        count = queryset(**filter).count()
        return count