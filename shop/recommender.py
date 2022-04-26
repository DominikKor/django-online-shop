import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender:
    @staticmethod
    def get_product_key(id_):
        return f'product:{id_}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if with_id != product_id:
                    # increment score for products purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only one product
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_ids = "".join([str(id_) for id_ in product_ids])
            tmp_key = f"tmp_{flat_ids}"
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id_) for id_ in product_ids]
            r.zunionstore(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id_) for id_ in suggestions]
