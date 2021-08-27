# Default Django import
from django.db import models

# Imports for Simple Cache
from django.utils import timezone
from django.db import DatabaseError, transaction


# Create the model for our cache storage
class SimpleCacheDB(models.Model):
    # This is a custom created ID used to recall items
    cache_id = models.CharField(max_length=255)
    # This is the date and time when the cache will expire
    cache_duration = models.DateTimeField()
    # A text blob to store the cached item in
    cache_value = models.TextField()


# This class allows for storage in a DB driven cache
class SimpleCache:
 
    # Given a cache ID return the cache object or return False
    @staticmethod
    def get_cache(cache_id):

        # Attempt the get query and handle errors if they occur
        try:
            with transaction.atomic():
                # Get the cache object using the ID
                get_query = SimpleCacheDB.objects.filter(cache_id=cache_id).latest('id')
                # Return the cache object
                return get_query
        except Exception:
            # Return false if the query fails or the cache_id did not return a result
            return False

    # Create a new cache item
    @staticmethod
    def set_cache(
        cache_id,
        cache_duration=timezone.now() + timezone.timedelta(hours=1),
        cache_value=list()
    ):

        # Build the query of items to insert
        insert_query = SimpleCacheDB(
            cache_id=cache_id,
            cache_value=cache_value,
            cache_duration=cache_duration
        )

        # Set the query to active to track success of the insert
        insert_query.active = True

        # Attempt the query
        try:
            with transaction.atomic():
                # Write the data to the database
                insert_query.save()
        except DatabaseError:
            # If the insert query failed set our active state to False
            insert_query.active = False

        # Check the state of our query
        if insert_query.active:
            # If the active state of the query is True, meaning the query is successful, return the ID
            return cache_id
        else:
            # If the query fails return False
            return False

    # Check to see if the cache item exists and if it has expired
    def check_cache(self, cache_id):
        # Load the cache object
        cache_object = self.get_cache(cache_id)
        # Check to see if the loaded object exists or returned false
        if cache_object is not False:
            # Capture the current date/time stamp
            today_date = timezone.now()
            # Check to see if the cached date is older than the current date (if the cache expired)
            if cache_object.cache_duration <= today_date:
                # If the cache has expired, deleted the related database item
                self.clear_cache(cache_id)
                # Return false if a usable cache item is not available
                return False
            else:
                # Return true if a usable cache item is available
                return True
        else:
            # Return false if a usable cache item is not available
            return False

    # Clear or delete a specified cache item
    @staticmethod
    def clear_cache(cache_id):

        # Attempt to perform the delete query
        try:
            if cache_id == 'ALL':
                # Load the cache item as an object based on the cache ID
                cache_item = SimpleCacheDB.objects.filter()
            else:
                # Load the cache item as an object based on the cache ID
                cache_item = SimpleCacheDB.objects.filter(cache_id=cache_id)
            # Delete the cache item
            cache_item.delete()
            # Return True to indicate that the delete operation was successful
            return True
        except Exception:
            # If the delete operation fails, return False
            return False
